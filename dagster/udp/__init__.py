from dagster import Definitions, load_assets_from_package_module

# User Code
from udp import assets
from .resources.rabbitmq_channel import rabbitmq_channel_resource
from .jobs import create_iot_data_job
from .schedules.iot_data_producer_schedule import iot_data_producer_schedule

all_resources = {"rabbitmq_channel": rabbitmq_channel_resource}
all_assets = load_assets_from_package_module(assets)
all_jobs = [create_iot_data_job]
all_schedules = [iot_data_producer_schedule]

definitions = Definitions(
    resources= all_resources,
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules
)
