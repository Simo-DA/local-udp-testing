from dagster import ScheduleDefinition
from ..jobs import create_iot_data_job

iot_data_producer_schedule = ScheduleDefinition(
    job=create_iot_data_job,
    cron_schedule="1/1 * * * *",  # every minute
)
