import json
import random
from typing import Union
import uuid
import time


def mock_iot_message(device_id: str) -> dict[str, Union[str, float, int]]:
    try:
        id = str(uuid.uuid4())
        temperature = 10.0 + random.uniform(-15.0, 15.0)
        timestamp = time.time()
        message = json.dumps(
            {
                "device_id": device_id,
                "id": id,
                "temperature": temperature,
                "timestamp": timestamp,
            }
        )
    except Exception as e:
        print(f"Error in mock_iot_message: {e}")
    finally:
        return message
