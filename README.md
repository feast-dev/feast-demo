# Feast demo

## Overview

This tutorial demonstrates the use of on demand feature views and stream ingestion in Feast. It extends the Feast default demo data to
include on demand transformations and pushing to the online store from stream events.

It also includes miscellaneous code samples for embedding in tutorials / blog posts.

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
Created entity driver
Created feature view driver_hourly_stats
Created on demand feature view transformed_conv_rate

Created sqlite table feast_demo_driver_hourly_stats
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
      driver_id           event_timestamp  val_to_add  val_to_add_2 string_feature  conv_rate  acc_rate  avg_daily_trips  conv_rate_plus_val1  conv_rate_plus_val2
360        1001 2021-04-12 10:59:42+00:00           1            10           test   0.701558  0.195824              566             1.701558            10.701558
721        1002 2021-04-12 08:12:10+00:00           2            20           test   0.775499  0.947109              890             2.775499            20.775499
1082       1003 2021-04-12 16:40:26+00:00           3            30           test   0.186658  0.245490              971             3.186658            30.186658
1445       1004 2021-04-12 15:01:12+00:00           4            40           test   0.891017  0.118256              154             4.891017            40.891017

--- Online features ---
acc_rate  :  [0.8408732414245605]
avg_daily_trips  :  [714]
conv_rate_plus_val1  :  [1000.8123571872711]
conv_rate_plus_val2  :  [2000.8123571872711]
driver_id  :  [1001]
string_feature  :  ['test']

--- Simulate a stream event ingestion of the hourly stats df ---
   driver_id     event_timestamp             created  conv_rate  acc_rate  avg_daily_trips string_feature
0       1001 2021-05-13 10:59:42 2021-05-13 10:59:42        1.0       1.0             1000          test2

--- Online features again with updated values---
acc_rate  :  [1.0]
avg_daily_trips  :  [1000]
conv_rate_plus_val1  :  [1001.0]
conv_rate_plus_val2  :  [2001.0]
driver_id  :  [1001]
string_feature  :  ['test2']

```
