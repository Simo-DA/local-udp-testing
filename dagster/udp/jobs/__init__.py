from dagster import define_asset_job
from ..assets.mock_iot_data import mock_iot_data

create_iot_data_job = define_asset_job("create_iot_data_job", selection=[mock_iot_data])
