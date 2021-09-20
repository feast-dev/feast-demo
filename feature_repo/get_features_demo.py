from feast import FeatureStore
from datetime import datetime
import pandas as pd

store = FeatureStore(repo_path=".")

print("--- Historical features ---")
entity_df = pd.DataFrame.from_dict(
    {
        "driver_id": [1001, 1002, 1003, 1004],
        "event_timestamp": [
            datetime(2021, 4, 12, 10, 59, 42),
            datetime(2021, 4, 12, 8, 12, 10),
            datetime(2021, 4, 12, 16, 40, 26),
            datetime(2021, 4, 12, 15, 1, 12),
        ],
        "val_to_add": [1, 2, 3, 4],
        "val_to_add_2": [10, 20, 30, 40]
    }
)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
        "transformed_conv_rate:conv_rate_plus_val1",
        "transformed_conv_rate:conv_rate_plus_val2",
    ],
).to_df()
print(training_df.head())

print("\n--- Online features ---")
features = store.get_online_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
        "transformed_conv_rate:conv_rate_plus_val1",
        "transformed_conv_rate:conv_rate_plus_val2",
    ],
    entity_rows=[{"driver_id": 1001}, {"val_to_add": 1000}, {"val_to_add_2": 2000}],
).to_dict()
for key, value in features.items():
    print(key, ' : ', value)