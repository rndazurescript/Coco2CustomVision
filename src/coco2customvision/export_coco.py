from .integration import (
    ensure_custom_vision_tags_in_coco,
    add_custom_vision_tagged_images_to_coco,
)
from .coco import get_empty_coco_dataset
from .azure_blob import upload_as_json


def export_custom_vision_to_coco(
    custom_vision_client,
    custom_vision_project,
    blob_container_client,
    storage_path,
    coco_file_name,
):
    coco = get_empty_coco_dataset()
    available_tags = custom_vision_client.get_project_tags(custom_vision_project)
    ensure_custom_vision_tags_in_coco(coco, available_tags)
    images = custom_vision_client.get_tagged_images(custom_vision_project)
    add_custom_vision_tagged_images_to_coco(
        coco, images, blob_container_client, storage_path
    )
    file_name = coco_file_name
    if storage_path is not None and len(storage_path) > 0:
        file_name = f"{storage_path}{coco_file_name}"

    upload_as_json(blob_container_client, coco, file_name)
