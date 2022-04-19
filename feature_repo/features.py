from datetime import timedelta

import pandas as pd
from feast import (
    Entity,
    Feature,
    FeatureView,
    FeatureService,
    Field,
    FileSource,
    PushSource,
    RequestSource,
    ValueType,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64, String

driver_hourly_stats = FileSource(
    path="data/driver_stats_with_string.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
    description="A table describing the stats of a driver, such as the average daily number of trips.",
    owner="test@gmail.com",
)

driver_stats_push_source = PushSource(
    name="driver_stats_push_source", batch_source=driver_hourly_stats,
)

driver = Entity(
    name="driver",
    join_keys=["driver_id"],
    value_type=ValueType.INT64,
    description="driver id",
)

driver_hourly_stats_view = FeatureView(
    name="driver_hourly_stats",
    entities=["driver"],
    ttl=timedelta(seconds=8640000000),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
        Field(name="string_feature", dtype=String),
    ],
    online=True,
    source=driver_stats_push_source,
    tags={"production": "True"},
    owner="test2@gmail.com",
)

# Define a request data source which encodes features / information only
# available at request time (e.g. part of the user initiated HTTP request)
input_request = RequestSource(
    name="vals_to_add",
    schema=[
        Field(name="val_to_add", dtype=Int64),
        Field(name="val_to_add_2", dtype=Int64),
    ],
)

# Define an on demand feature view which can generate new features based on
# existing feature views and RequestSource features
@on_demand_feature_view(
    sources={
        "driver_hourly_stats": driver_hourly_stats_view,
        "vals_to_add": input_request,
    },
    schema=[
        Field(name="conv_rate_plus_val1", dtype=Float64),
        Field(name="conv_rate_plus_val2", dtype=Float64),
    ],
)
def transformed_conv_rate(inputs: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["conv_rate_plus_val1"] = inputs["conv_rate"] + inputs["val_to_add"]
    df["conv_rate_plus_val2"] = inputs["conv_rate"] + inputs["val_to_add_2"]
    return df


feature_service = FeatureService(
    name="convrate_plus100",
    features=[
        driver_hourly_stats_view[["conv_rate", "avg_daily_trips"]],
        transformed_conv_rate,
    ],
    owner="test3@gmail.com",
)
