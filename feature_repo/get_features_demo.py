from feast import FeatureStore
from datetime import datetime
import pandas as pd

def run_demo():
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
            "val_to_add_2": [10, 20, 30, 40],
            "driver_age": [10, 20, 30, 40],
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
            "driver_age:driver_age"
        ],
    ).to_df()
    print(training_df.head())

    print("\n--- Online features ---")
    features = store.get_online_features(
        features=[
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
            "transformed_conv_rate:conv_rate_plus_val1",
            "transformed_conv_rate:conv_rate_plus_val2",
            "driver_age:driver_age"
        ],
        entity_rows=[{"driver_id": 1001}, {"val_to_add": 1000}, {"val_to_add_2": 2000}, {"driver_age": 25}],
    ).to_dict()
    for key, value in sorted(features.items()):
        print(key, ' : ', value)


    print("\n--- Simulate a stream event ingestion of the hourly stats df ---")
    event_df = pd.DataFrame.from_dict(
        {
            "driver_id": [1001],
            "event_timestamp": [
                datetime(2021, 5, 13, 10, 59, 42),
            ],
            "created": [
                datetime(2021, 5, 13, 10, 59, 42),
            ],
            "conv_rate": [1.0],
            "acc_rate": [1.0],
            "avg_daily_trips": [1000],
        }
    )
    print(event_df)
    store.write_to_online_store("driver_hourly_stats", event_df)

    print("\n--- Online features again with updated values from a stream push---")
    features = store.get_online_features(
        features=[
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
            "transformed_conv_rate:conv_rate_plus_val1",
            "transformed_conv_rate:conv_rate_plus_val2",
            "driver_age:driver_age"
        ],
        entity_rows=[{"driver_id": 1001}, {"val_to_add": 1000}, {"val_to_add_2": 2000}, {"driver_age": 25}],
    ).to_dict()
    for key, value in sorted(features.items()):
        print(key, ' : ', value)


if __name__ == "__main__":
    run_demo()