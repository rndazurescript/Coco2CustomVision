from coco2customvision.export_coco import export_custom_vision_to_coco


def test_can_dump_project_into_coco(
    custom_vision_client, custom_vision_project, blob_container_client
):
    target_file_name = "coco_dataset.json"
    target_path = None
    export_custom_vision_to_coco(
        custom_vision_client,
        custom_vision_project,
        blob_container_client,
        target_path,
        target_file_name,
    )
