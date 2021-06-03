from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
    generate_container_sas,
    ContainerSasPermissions,
)
from datetime import datetime, timedelta
import time
from .utils import serialize_to_stream
import json


def get_blob_container_client(account_name, account_key, container_name):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net/",
        credential=account_key,
    )
    return blob_service_client.get_container_client(container_name)


def wait_for_copy(blob):
    count = 0
    props = blob.get_blob_properties()
    while props.copy.status == "pending":
        count = count + 1
        if count > 10:
            raise TimeoutError("Timed out waiting for async copy to complete.")
        time.sleep(5)
        props = blob.get_blob_properties()
    return props


def upload_as_json(blob_container_client, object, blob_path):
    object_stream = serialize_to_stream(object)
    blob_client = blob_container_client.get_blob_client(blob_path)
    blob_client.upload_blob(object_stream.getvalue(), overwrite=True)


def download_json(blob_container_client, blob_path):
    blob_client = blob_container_client.get_blob_client(blob_path)
    json_blob = blob_client.download_blob()
    json_bytes = json_blob.readall()
    object = json.loads(json_bytes)
    return object


def get_blob_sas_token(blob, for_x_hours=1):
    return generate_blob_sas(
        account_name=blob.account_name,
        account_key=blob.credential.account_key,
        container_name=blob.container_name,
        blob_name=blob.blob_name,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=for_x_hours),
    )


def get_container_sas_token(blob_container_client, for_x_hours=1):
    return generate_container_sas(
        blob_container_client.account_name,
        blob_container_client.container_name,
        account_key=blob_container_client.credential.account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=for_x_hours),
    )
