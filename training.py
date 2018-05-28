import csv

import dill
import logging
import numpy

from config import DILL_MODEL_FILE, AGGREGATED_DATA_FILE, PREDICTED_CLV_FILE


logger = logging.getLogger(__name__)


def train_model(model_file=DILL_MODEL_FILE,
                agg_data_file=AGGREGATED_DATA_FILE,
                output_file=PREDICTED_CLV_FILE):
    """
    Loads the model from the dill file, and uses it's *predict* method for
    every row of aggregated data. Saves the results into a separate csv-file.
    :param model_file: path to the dill model file
    :param agg_data_file: path to the aggregated data file
    :param output_file: path to the output file
    """
    with open(output_file, 'w') as output, open(agg_data_file) as agg_csv:
        # fill the headers for outout file
        output_headers = ('customer_id', 'predicted_clv')
        output_writer = csv.DictWriter(output, fieldnames=output_headers)
        output_writer.writeheader()

        # load the model from dill file
        with open(model_file, 'rb') as model_file:
            model = dill.load(model_file)

        # start reading aggregated data
        csv_reader = csv.reader(agg_csv)
        next(csv_reader, None)  # skip the headers of aggregated data file
        for row in csv_reader:
            # detach customer_id from the other data
            customer_id = row[0]

            # convert all values into float and wrap into numpy 2d array
            arr = numpy.asanyarray([[float(r) for r in row[1:]]])

            # make clv prediction
            predicted_clv = model.predict(arr)
            assert len(predicted_clv) == 1, "Error in prediction. " \
                                            "Should return 1-element array"
            # save prediction into output file
            output_writer.writerow(
                {"customer_id": customer_id,
                 "predicted_clv": predicted_clv[0]})

    logger.info("Training finished succesfully")


if __name__ == '__main__':
    train_model()
