from .integration import (
    get_category_id_to_tag_id_dictionary,
    image_annotations_to_region,
)
from .azure_blob import download_json, get_container_sas_token
from tqdm import tqdm
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageUrlCreateEntry,
)


def import_coco_to_custom_vision(
    custom_vision_client,
    custom_vision_project,
    blob_container_client,
    storage_path,
    coco_file_name,
):
    # Read coco dataset definition
    file_name = coco_file_name
    if storage_path is not None and len(storage_path) > 0:
        file_name = f"{storage_path}{coco_file_name}"
    coco_dataset = download_json(blob_container_client, file_name)

    category_id_to_tag_id_dictionary = get_category_id_to_tag_id_dictionary(
        coco_dataset, custom_vision_client, custom_vision_project
    )

    container_sas_token = get_container_sas_token(blob_container_client)

    images_to_upload = []
    for image in tqdm(
        coco_dataset["images"],
        ascii=True,
        desc="Preparing coco images",
    ):
        image_url = f"{image['coco_url']}?{container_sas_token}"
        regions = image_annotations_to_region(
            coco_dataset["annotations"], image, category_id_to_tag_id_dictionary
        )
        images_to_upload.append(ImageUrlCreateEntry(url=image_url, regions=regions))

    custom_vision_client.upload_images_from_url(custom_vision_project, images_to_upload)
