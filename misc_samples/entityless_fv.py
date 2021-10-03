global_stats_fv = FeatureView(
    name="global_stats",
    entities=[],
    features=[
        Feature(name="total_trips_today_by_all_drivers", dtype=ValueType.INT64),
    ],
    batch_source=BigQuerySource(
        table_ref="feast-oss.demo_data.global_stats"
    )
)