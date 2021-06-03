import pytest
import os

ENV_KEY_PARAM = "STORAGE_ACCOUNT_KEY"
ENV_NAME_PARAM = "STORAGE_ACCOUNT_NAME"
ENV_CONTAINER_NAME_PARAM = "STORAGE_ACCOUNT_CONTAINER_NAME"


@pytest.fixture
def blob_container_client():
    from coco2customvision.azure_blob import get_blob_container_client

    account_key = os.environ[ENV_KEY_PARAM]
    account_name = os.environ[ENV_NAME_PARAM]
    container_name = os.environ[ENV_CONTAINER_NAME_PARAM]
    client = get_blob_container_client(account_name, account_key, container_name)
    assert (
        client is not None
    ), f"Failed to instantiate container service client for container {container_name}"
    return client
