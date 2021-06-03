from coco2customvision.integration import get_category_id_to_tag_id_dictionary


def test_cat_get_category_id_to_tag_id_dictionary(
    custom_vision_client, custom_vision_project
):
    test_tag_1_id = 1
    test_tag_1_name = "Tag 1"
    test_tag_2_id = 2
    test_tag_2_name = "Tag 2"

    coco_dataset = {
        "categories": [
            {"id": test_tag_1_id, "name": test_tag_1_name, "supercategory": "Root"},
            {"id": test_tag_2_id, "name": test_tag_2_name, "supercategory": "Root"},
        ]
    }
    dictionary = get_category_id_to_tag_id_dictionary(
        coco_dataset, custom_vision_client, custom_vision_project
    )
    tags_id_dictionary = custom_vision_client.get_project_tags_by_id(
        custom_vision_project
    )

    assert dictionary is not None, "Failed to retrieve annotations dictionary"
    assert len(dictionary) == 2, "Dictionary doesn't have 2 elements as expected"
    dictionary_keys = list(dictionary.keys())
    assert (
        dictionary_keys[0] == test_tag_1_id and dictionary_keys[1] == test_tag_2_id
    ), "Category keys not found"
    assert (
        tags_id_dictionary[dictionary[test_tag_1_id]].name == test_tag_1_name
        and tags_id_dictionary[dictionary[test_tag_2_id]].name == test_tag_2_name
    ), "Category tags are wrong"
