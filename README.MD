**Lesara test assignment.**

To start application with the docker use the following command:
```make server-start```
After that you could reach the application with requests like this:
```http://0.0.0.0:8000/clv?customer_id=d0d7a76fea3729a9381d39aca78b52d3```

Response example:
```
{
    "predicted_clv": "151.36"
}
```

Use the following command to run unittests:
```make unittest```


**What this application is actually doing?**
0) starts docker container where everything will be working

1) ```etl.py``` script is launched. It transforms data from ```input_files/orders.csv``` 
and saves as ```output_files/aggregated_data.csv```. Resulting file has format 
needed for prediction model: each row has customer_id and 6 metrics for 
prediction (*total_orders,order_revenue_max,revenue_total,num_items_max,days_from_last_order,longest_interval*)

2) ```training.py``` script is launched. It loads the model instance from the dill-file 
(```input_files/model.dill```) and for each row in ```output_files/aggregated_data.csv```
calls *predict* function of the model. Resulting predictions are stored in ```output_files/predicted_clv.csv```.
The file has only 2 columns: *customer_id* and *predicted_clv*.

3) flask application is started from ```application.py```. Application has only 1 GET-endpoint - */clv*.
You must provide *customer_id* required query-parameter.
In order to serve quickly, application has a dict-like cache for the data
from ```output_files/predicted_clv.csv```, where keys are customer_id's and predicted clv's are values. 


*NB: I've realised at the very last moment that I understood incorrectly how to handle
longest interval for customers with 1 order. I thought it must be only "days since last order".
So, I calculated avg(longest interval for customers with at least 2 orders) manually 
and used it as a constant in code (see AVG_LONGEST_INTERVAL in config.py)*