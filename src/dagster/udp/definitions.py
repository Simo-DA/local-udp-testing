from dagster import Definitions, load_assets_from_package_module

# Assets
import assets

# resources
from resources.RabbitmqChannel import RabbitmqChannel
from resources.s3_client import s3_client

# jobs
from jobs import produce_iot_data

# schedule
from schedules.iot_data_producer_schedule import iot_data_producer_schedule

all_resources = {
    "rabbitmq_channel": RabbitmqChannel(),
    "s3_client": s3_client,
}
all_assets = load_assets_from_package_module(assets)
all_jobs = [produce_iot_data]
all_schedules = [iot_data_producer_schedule]

definitions = Definitions(
    resources=all_resources, assets=all_assets, jobs=all_jobs, schedules=all_schedules
)
