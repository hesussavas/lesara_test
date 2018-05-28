import logging
from datetime import datetime

import pandas as pd

from config import TERMINAL_DATE, DATE_FORMAT, ORDERS_CSV_FILE, \
    AGGREGATED_DATA_FILE, AVG_LONGEST_INTERVAL

logger = logging.getLogger(__name__)


def _days_since_last_order(orders_dates):
    """
    Returns difference in days between terminal_date (right now - '2017-10-17')
    and the oldest inputted order_date.
    :param orders_dates: iterable with sorted dates as strings in proper
    format. If format is not correct - will return 0.
    :return: integer - difference in days
    """
    last_order_date = max(orders_dates)
    try:
        terminal_date = datetime.strptime(TERMINAL_DATE, DATE_FORMAT)
        last_order_date = datetime.strptime(last_order_date,
                                            DATE_FORMAT)
    except ValueError as err:
        # in case of wrong date format - report error and return 0.
        logger.error(err)
        return 0

    return (terminal_date - last_order_date).days


def _longest_interval(orders_dates):
    """
    Calculates the longest interval between 2 consecutive order dates in days.
    If customer has only 1 order - returns
    days_since_last_order + avg(longest_interval)
    :param orders_dates: iterable with sorted dates as strings in proper
    format. If format is not correct - will return 0.
    :return: integer - the longest interval between 2 orders in days
    """
    if len(orders_dates) == 1:
        return AVG_LONGEST_INTERVAL + _days_since_last_order(orders_dates)

    # convert strings in to datetime in order to compare intervals
    try:
        orders_dates = [datetime.strptime(order_date, DATE_FORMAT) for
                        order_date in orders_dates]
    except ValueError as err:
        # in case of wrong date format - report error and return 0.
        logger.error(err)
        return 0

    # find the longest interval
    difference = 0
    first_date = orders_dates[0]
    for next_date in orders_dates[1:]:
        new_difference = (next_date - first_date).days
        if new_difference > difference:
            difference = new_difference
            first_date = next_date
    return difference


def aggregate_data(orders_file=ORDERS_CSV_FILE,
                   output_file=AGGREGATED_DATA_FILE):
    """
    Simple ETL function.

    It reads 'orders.csv' file. Then aggregates data on
    per-order basis in order to have following pre-aggregated data:
    "Max number of items in one order", "Max revenue in one order" and
    "Sum of revenue for all items in order".

    After that it aggregates this data on per-customer basis, calculating all
    metrics needed for prediction.

    Finally, it dumped aggregated data into another csv-file.
    """

    orders = pd.read_csv(orders_file)

    # replace NaN values with 0, if any
    orders = orders.fillna(0)

    # per-order basis aggregation
    grouped_by_order = orders.groupby(
        by=['order_id', 'customer_id', 'created_at_date'],
        as_index=False).aggregate(
        {"revenue": ['max', 'sum'],
         "num_items": "max"})

    # rename columns for easy access
    grouped_by_order.columns = ["_".join(x) for x in
                                grouped_by_order.columns.ravel()]

    # per-customer basis aggregation
    grouped_by_customer = grouped_by_order.groupby(
        by=['customer_id_']).aggregate(
        {"order_id_": "count",
         "revenue_max": "max",
         "revenue_sum": "sum",
         "num_items_max": "max",
         "created_at_date_": [_days_since_last_order, _longest_interval]})

    # rename columns
    grouped_by_customer.columns = ["total_orders",
                                   "order_revenue_max",
                                   "revenue_total",
                                   "num_items_max",
                                   "days_from_last_order",
                                   "longest_interval"]

    # output data into the csv-file
    grouped_by_customer.to_csv(output_file)

    logger.info("Etl finished succesfully")


if __name__ == '__main__':
    aggregate_data()
