from dagster import Definitions, load_assets_from_package_module

# User Code
import assets
from resources.RabbitmqChannel import RabbitmqChannel
from jobs import produce_iot_data
from schedules.iot_data_producer_schedule import iot_data_producer_schedule

all_resources = {"rabbitmq_channel": RabbitmqChannel()}
all_assets = load_assets_from_package_module(assets)
all_jobs = [produce_iot_data]
all_schedules = [iot_data_producer_schedule]

definitions = Definitions(
    resources=all_resources, assets=all_assets, jobs=all_jobs, schedules=all_schedules
)
