from dagster import define_asset_job
from assets.rabbit_mq_producer import rabbit_mq_producer

produce_iot_data = define_asset_job("produce_iot_data", selection=[rabbit_mq_producer])
