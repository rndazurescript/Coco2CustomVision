import logging
import click
from .version import __version__
from .azure_blob import get_blob_container_client
from .custom_vision import ObjectDetectionTrainer
from .export_coco import export_custom_vision_to_coco
from .import_coco import import_coco_to_custom_vision


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Version {__version__}")
    ctx.exit()


@click.group(chain=True)
@click.option("--verbose", "-V", count=True, default=0, help="Verbose outputs")
@click.option(
    "--version",
    "-v",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
def cli(verbose):
    log_format = "[%(asctime)s][%(threadName)s][%(levelname)s][%(module)s.%(funcName)s:%(lineno)d] %(message)s"
    level = logging.ERROR
    if verbose == 1:
        level = logging.WARNING
    elif verbose == 2:
        level = logging.INFO
    elif verbose == 3:
        level = logging.DEBUG
    logging.basicConfig(level=level, format=log_format)


@cli.command(name="export")
@click.argument("coco_dataset_file_name")
@click.option(
    "-sk",
    "--storage-key",
    hide_input=True,
    help="Storage account key to read from/export to the coco dataset",
)
@click.option(
    "-sn",
    "--storage-name",
    help="Storage account name to read from/export to the coco dataset",
)
@click.option(
    "-sc",
    "--storage-container",
    help="Storage account container name to read from/export to the coco dataset",
)
@click.option(
    "-sp",
    "--storage-path",
    default=None,
    help="Path within the storage account container to read from/export to the coco dataset",
)
@click.option(
    "-cvk",
    "--custom-vision-key",
    hide_input=True,
    help="Custom vision account key from https://www.customvision.ai/projects#/settings",
)
@click.option(
    "-cve",
    "--custom-vision-endpoint",
    help="Custom vision account endpoint from https://www.customvision.ai/projects#/settings",
)
@click.option(
    "-cvp",
    "--custom-vision-project-name",
    help="Custom vision project name",
)
def export_cmd(
    storage_key,
    storage_name,
    storage_container,
    storage_path,
    custom_vision_key,
    custom_vision_endpoint,
    custom_vision_project_name,
    coco_dataset_file_name,
):
    """Exports a custom vision project to an Azure Blob container.
    COCO_DATASET_FILE_NAME is the name of the COCO json file.
    """
    blob_container_client = get_blob_container_client(
        storage_name, storage_key, storage_container
    )
    custom_vision_client = ObjectDetectionTrainer(
        custom_vision_key, custom_vision_endpoint
    )
    custom_vision_project = custom_vision_client.get_or_create_project(
        custom_vision_project_name
    )
    export_custom_vision_to_coco(
        custom_vision_client,
        custom_vision_project,
        blob_container_client,
        storage_path,
        coco_dataset_file_name,
    )


@cli.command(name="import")
@click.argument("coco_dataset_file_name")
@click.option(
    "-sk",
    "--storage-key",
    hide_input=True,
    help="Storage account key to read from the coco dataset",
)
@click.option(
    "-sn",
    "--storage-name",
    help="Storage account name to read from the coco dataset",
)
@click.option(
    "-sc",
    "--storage-container",
    help="Storage account container name to read from the coco dataset",
)
@click.option(
    "-sp",
    "--storage-path",
    default=None,
    help="Path within the storage account container to read fromthe coco dataset",
)
@click.option(
    "-cvk",
    "--custom-vision-key",
    hide_input=True,
    help="Custom vision account key from https://www.customvision.ai/projects#/settings",
)
@click.option(
    "-cve",
    "--custom-vision-endpoint",
    help="Custom vision account endpoint from https://www.customvision.ai/projects#/settings",
)
@click.option(
    "-cvp",
    "--custom-vision-project-name",
    help="Custom vision project name",
)
def import_cmd(
    storage_key,
    storage_name,
    storage_container,
    storage_path,
    custom_vision_key,
    custom_vision_endpoint,
    custom_vision_project_name,
    coco_dataset_file_name,
):
    """Exports a custom vision project to an Azure Blob container.
    COCO_DATASET_FILE_NAME is the name of the COCO json file.
    """
    blob_container_client = get_blob_container_client(
        storage_name, storage_key, storage_container
    )
    custom_vision_client = ObjectDetectionTrainer(
        custom_vision_key, custom_vision_endpoint
    )
    custom_vision_project = custom_vision_client.get_or_create_project(
        custom_vision_project_name
    )
    import_coco_to_custom_vision(
        custom_vision_client,
        custom_vision_project,
        blob_container_client,
        storage_path,
        coco_dataset_file_name,
    )
