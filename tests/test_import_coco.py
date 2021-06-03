from coco2customvision.import_coco import import_coco_to_custom_vision


def test_can_create_project_from_coco(
    custom_vision_client, custom_vision_project, blob_container_client
):
    target_file_name = "coco_dataset.json"
    target_path = None
    import_coco_to_custom_vision(
        custom_vision_client,
        custom_vision_project,
        blob_container_client,
        target_path,
        target_file_name,
    )
