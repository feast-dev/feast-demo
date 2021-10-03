$ feast init feature_repo
Creating a new Feast repository in /home/tsotne/feast/feature_repo.

$ cd feature_repo

$ feast apply
Registered entity driver_id
Registered feature view driver_hourly_stats
Deploying infrastructure for driver_hourly_stats

$ feast materialize-incremental $(date +%Y-%m-%d)
Materializing 1 feature views to 2021-09-09 17:00:00-07:00 into the sqlite online store.

driver_hourly_stats from 2021-09-09 16:51:08-07:00 to 2021-09-09 17:00:00-07:00:
100%|████████████████████████████████████████████████████████████████| 5/5
[00:00<00:00, 295.24it/s]

$ feast serve
# This is an experimental feature. It's intended for early testing and feedback, and could
# change without warnings in future releases.
INFO:     Started server process [8889]
09/10/2021 10:42:11 AM INFO:Started server process [8889]
INFO:     Waiting for application startup.
    09/10/2021 10:42:11 AM INFO:Waiting for application startup.
    INFO:     Application startup complete.
09/10/2021 10:42:11 AM INFO:Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:6566 (Press CTRL+C to quit)
09/10/2021 10:42:11 AM INFO:Uvicorn running on http://127.0.0.1:6566 (Press CTRL+C to quit)