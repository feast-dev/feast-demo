# On demand feature views demo

## Overview

This tutorial demonstrates the use of on demand feature views in Feast. It extends the Feast default demo data to
include on demand transformations.

## Setup

### Setting up Feast

Install Feast using pip

```
pip install feast
```

We have already set up a feature repository in [feature_repo/](feature_repo/). 

Deploy the feature store by running `apply` from within the `feature_repo/` folder
```
cd feature_repo/
feast apply
```

Output:
```
Registered entity driver_id
Registered feature view driver_hourly_stats
Registered on demand feature view transformed_conv_rate
Deploying infrastructure for driver_hourly_stats
```

Next we load features into the online store using the `materialize-incremental` command. This command will load the
latest feature values from a data source into the online store.

```
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
```

Output:
```
Materializing 1 feature views to 2021-09-20 13:36:06-04:00 into the sqlite online store.

driver_hourly_stats from 2021-06-12 17:43:32-04:00 to 2021-09-20 13:36:06-04:00:
100%|███████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 1509.29it/s]
```

## Fetch features

```
python get_features_demo.py
```

Output:
```
--- Historical features ---
            event_timestamp  driver_id  val_to_add  val_to_add_2  ...  acc_rate  avg_daily_trips  conv_rate_plus_val1  conv_rate_plus_val2
0 2021-04-12 08:12:10+00:00       1002           2            20  ...  0.947109              890             2.775499            20.775499
1 2021-04-12 10:59:42+00:00       1001           1            10  ...  0.195824              566             1.701558            10.701558
2 2021-04-12 15:01:12+00:00       1004           4            40  ...  0.118256              154             4.891017            40.891017
3 2021-04-12 16:40:26+00:00       1003           3            30  ...  0.245490              971             3.186658            30.186658

[4 rows x 10 columns]

--- Online features ---
conv_rate  :  [0.8123572]
acc_rate  :  [0.84087324]
driver_id  :  [1001]
conv_rate_plus_val1  :  [1000.8123572]
conv_rate_plus_val2  :  [2000.8123572]
driver_age  :  [25]
avg_daily_trips  :  [714]
```