import logging
from .coco import get_max_id
from .azure_blob import wait_for_copy
from tqdm import tqdm
from azure.cognitiveservices.vision.customvision.training.models import Region

log = logging.getLogger(__name__)


def ensure_custom_vision_tags_in_coco(
    coco_dataset, custom_vision_project_tags, super_category_name="Root"
):
    """Ensures that all tags from custom vision project exist in the COCO dataset"""
    coco_section = coco_dataset["categories"]
    max_category_id = get_max_id(coco_section)
    coco_existing_category_names = (t.name for t in coco_section)
    for tag in tqdm(
        custom_vision_project_tags,
        ascii=True,
        desc="Parsing custom vision project tags",
    ):
        if tag.name not in coco_existing_category_names:
            max_category_id = max_category_id + 1
            category_data = {
                "id": max_category_id,
                "name": tag.name,
                "supercategory": super_category_name,
            }
            coco_section.append(category_data)
            # No need to keep it in the list since
            # tag names can appear only once
            # coco_existing_category_names.append(tag.name)
        else:
            log.info(f"Category {tag.name} exists in COCO dataset.")


def add_custom_vision_tagged_images_to_coco(
    coco_dataset, custom_vision_images, blob_container_client, upload_to_folder=""
):
    image_entries = []
    annotation_entries = []
    max_image_id = get_max_id(coco_dataset["images"])
    max_annotation_id = get_max_id(coco_dataset["annotations"])

    tag_ids = (t["id"] for t in coco_dataset["categories"])
    tag_names = (t["name"] for t in coco_dataset["categories"])
    tags_dictionary = dict(zip(tag_names, tag_ids))

    for image in tqdm(custom_vision_images, ascii=True, desc="Processing images"):
        max_image_id = max_image_id + 1
        blob_name = f"{max_image_id:012d}.jpg"
        if upload_to_folder is not None and len(upload_to_folder) > 0:
            blob_name = f"{upload_to_folder}/{blob_name}"

        blob_client = blob_container_client.get_blob_client(blob_name)
        blob_url = blob_client.url.split("?")[0]

        image_data = {
            "id": max_image_id,
            "width": image.width,
            "height": image.height,
            "file_name": blob_name,
            "license": 1,
            "coco_url": blob_url,
        }

        image_entries.append(image_data)

        for region in image.regions:
            max_annotation_id = max_annotation_id + 1
            # Find category_id based on the region tag
            category_id = tags_dictionary.get(region.tag_name)
            # The COCO bounding box format is [top left x position, top left y position, width, height].
            bbox = [
                region.left * image.width,
                region.top * image.height,
                region.width * image.width,
                region.height * image.height,
            ]
            # Calculate area as de-normalized length*width
            area = region.width * image.width * region.height * image.height
            annotation_data = {
                "id": max_annotation_id,
                "image_id": max_image_id,
                "category_id": category_id,
                "iscrowd": 0,
                "bbox": bbox,
                "area": area,
                "segmentation": [],
            }
            annotation_entries.append(annotation_data)

            blob_client.start_copy_from_url(
                image.original_image_uri, metadata=image.metadata
            )
            wait_for_copy(blob_client)

    coco_dataset["images"].extend(image_entries)
    coco_dataset["annotations"].extend(annotation_entries)


def get_category_id_to_tag_id_dictionary(
    coco_dataset, custom_vision_client, custom_vision_project
):
    coco_category_names = list(t["name"] for t in coco_dataset["categories"])
    tags_name_dictionary = custom_vision_client.get_project_tags_by_name(
        custom_vision_project, ensure_tag_names=coco_category_names
    )
    tag_ids = []
    for category_name in coco_category_names:
        tag_ids.append(tags_name_dictionary[category_name].id)
    coco_category_ids = (t["id"] for t in coco_dataset["categories"])
    return dict(zip(coco_category_ids, tag_ids))


def image_annotations_to_region(
    coco_annotations, coco_image, category_id_to_tag_id_dictionary
):
    regions = []
    image_id = coco_image["id"]
    image_width = coco_image["width"]
    image_height = coco_image["height"]
    for annotation in filter(lambda x: x["image_id"] == image_id, coco_annotations):
        if annotation["category_id"] is not None:
            tag_id = category_id_to_tag_id_dictionary[annotation["category_id"]]
            bbox_left = annotation["bbox"][0] / image_width
            bbox_top = annotation["bbox"][1] / image_height
            bbox_width = annotation["bbox"][2] / image_width
            bbox_height = annotation["bbox"][3] / image_height
            region = Region(
                tag_id=tag_id,
                left=bbox_left,
                top=bbox_top,
                width=bbox_width,
                height=bbox_height,
            )
            regions.append(region)
    return regions
