from dagster import ScheduleDefinition
from jobs import produce_iot_data

iot_data_producer_schedule = ScheduleDefinition(
    job=produce_iot_data,
    cron_schedule="1/1 * * * *",  # every minute
)
