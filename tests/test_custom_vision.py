import os
import pytest

ENV_KEY_PARAM = "CUSTOM_VISION_KEY"
ENV_ENDPOINT_PARAM = "CUSTOM_VISION_ENDPOINT"
PROJECT_NAME = "PYTEST_PROJECT"
TAG_TO_CREATE = "test tag 1"


@pytest.fixture
def custom_vision_client():
    from coco2customvision import ObjectDetectionTrainer

    cv_key = os.environ[ENV_KEY_PARAM]
    cv_endpoint = os.environ[ENV_ENDPOINT_PARAM]
    client = ObjectDetectionTrainer(cv_key, cv_endpoint)
    assert client is not None, "Failed to instantiate custom vision client"
    return client


@pytest.fixture
def custom_vision_project(custom_vision_client):
    return custom_vision_client.get_or_create_project(PROJECT_NAME)


def test_ObjectDetectionTrainer_can_get_project(custom_vision_project):
    assert custom_vision_project is not None, f"Failed to get or create {PROJECT_NAME}"


def test_ObjectDetectionTrainer_can_get_tags(
    custom_vision_client, custom_vision_project
):
    available_tags = custom_vision_client.get_project_tags(custom_vision_project)
    assert available_tags is not None, f"Failed to retrieve tags in {PROJECT_NAME}"


def test_ObjectDetectionTrainer_can_get_tags_by_name(
    custom_vision_client, custom_vision_project
):
    available_tags = custom_vision_client.get_project_tags_by_name(
        custom_vision_project, [TAG_TO_CREATE]
    )
    assert available_tags is not None, f"Failed to retrieve tags in {PROJECT_NAME}"
    assert (
        available_tags[TAG_TO_CREATE] is not None
    ), f"{TAG_TO_CREATE} dictionary entry has no object"
    assert (
        available_tags[TAG_TO_CREATE].name == TAG_TO_CREATE
    ), f"{TAG_TO_CREATE} != {available_tags[TAG_TO_CREATE].name}"


def test_ObjectDetectionTrainer_can_get_tags_by_id(
    custom_vision_client, custom_vision_project
):
    available_tags = custom_vision_client.get_project_tags_by_id(
        custom_vision_project, [TAG_TO_CREATE]
    )
    assert available_tags is not None, f"Failed to retrieve tags in {PROJECT_NAME}"
    test_tag_tuple = next(
        filter(lambda elem: elem[1].name == TAG_TO_CREATE, available_tags.items())
    )
    assert (
        test_tag_tuple is not None and test_tag_tuple[1] is not None
    ), f"Failed to retrieve tag {TAG_TO_CREATE} in {PROJECT_NAME}"
    test_tag = test_tag_tuple[1]
    assert (
        available_tags[test_tag.id] is test_tag
    ), f"{test_tag.id} dictionary entry is not pointing to the {TAG_TO_CREATE} tag"
