from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageUrlCreateBatch,
)
from msrest.authentication import ApiKeyCredentials
from abc import ABC, abstractmethod
import logging
from .utils import batch

log = logging.getLogger(__name__)


class AbstractTrainer(ABC):
    """
    Responsible for interactions with the training API of Custom Vision.
    Get the key and the endpoint from the project settings at https://www.customvision.ai/.
    """

    def __init__(self, key, endpoint):
        self.client = CustomVisionTrainingClient(
            endpoint=endpoint,
            credentials=ApiKeyCredentials(in_headers={"Training-key": key}),
        )

    @abstractmethod
    def create_project(self, project_name, domain="General"):
        pass

    def get_project_tags_by_name(self, project, ensure_tag_names=[]):
        available_tags = self.get_project_tags(project, ensure_tag_names)
        tag_names = (t.name for t in available_tags)
        return dict(zip(tag_names, available_tags))

    def get_project_tags_by_id(self, project, ensure_tag_names=[]):
        available_tags = self.get_project_tags(project, ensure_tag_names)
        tag_ids = (t.id for t in available_tags)
        return dict(zip(tag_ids, available_tags))

    def get_project_tags(self, project, ensure_tag_names=[]):
        """Retrieves or creates the tags from Custom Vision project"""
        available_tags = self.client.get_tags(project.id)
        for tag_name in ensure_tag_names:
            tag = next(filter(lambda x: x.name == tag_name, available_tags), None)
            if tag is None:
                log.info(
                    f"Tag '{tag_name}' not found in project '{project.name}'. Creating it."
                )
                self.client.create_tag(project.id, tag_name)
        return self.client.get_tags(project.id)

    def get_or_create_project(self, project_name):
        available_projects = self.client.get_projects()
        project = next(
            filter(lambda x: x.name == project_name, available_projects), None
        )
        if project is None:
            log.info(f"Project '{project_name}' not found. Creating it.")
            project = self.create_project(project_name)
        return project

    def get_tagged_images(self, project, take=-1, skip=0, tag_ids_to_filter_for=None):
        """You can potentially use a DONE tag to tag images that are fully done (all objects tagged) and you
        can be reading only those images. Pass 0 or negative in take to get all images"""
        # The REST API can pull up to 256 images
        if take > 0 and take <= 256:
            return self.client.get_tagged_images(
                project.id, take=take, skip=skip, tag_ids=tag_ids_to_filter_for
            )
        else:
            # Pull using take and skip
            current_skip = skip
            current_take = 256
            was_last_call = False
            output = []
            images = self.client.get_tagged_images(
                project.id,
                take=current_take,
                skip=current_skip,
                tag_ids=tag_ids_to_filter_for,
            )
            while len(images) > 0:
                output.extend(images)
                current_skip += current_take
                if take > 256:
                    take -= 256
                elif take > 0:
                    current_take = take
                    was_last_call = True
                if was_last_call:
                    images = []
                else:
                    images = self.client.get_tagged_images(
                        project.id,
                        take=current_take,
                        skip=current_skip,
                        tag_ids=tag_ids_to_filter_for,
                    )
            return output

    def upload_images_from_url(self, project, image_url_entries):
        for image_url_entries_batch in batch(
            image_url_entries, 64, "Uploading image batch"
        ):
            batch_load = ImageUrlCreateBatch(images=image_url_entries_batch)
            upload_process = self.client.create_images_from_urls(project.id, batch_load)
            if not upload_process.is_batch_successful:
                for image in upload_process.images:
                    image_url = image.source_url.split("?")[0]
                    status = image.status
                    log.error(
                        f"Failed to upload image {image_url} with status {status}"
                    )


class ObjectDetectionTrainer(AbstractTrainer):
    PROJECT_TYPE = "ObjectDetection"

    def create_project(self, project_name, domain="General"):
        available_domains = self.client.get_domains()
        selected_domain = next(
            filter(
                lambda x: x.type == self.PROJECT_TYPE and x.name == domain,
                available_domains,
            ),
            None,
        )
        if selected_domain is None:
            raise Exception(
                f"Couldn't locate domain '{domain}' for project type '{self.PROJECT_TYPE}'."
            )
        return self.client.create_project(
            name=project_name, domain_id=selected_domain.id
        )
