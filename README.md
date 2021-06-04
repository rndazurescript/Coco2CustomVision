# Coco to Custom Vision (in Azure)

[![Build](https://github.com/rndazurescript/Coco2CustomVision/actions/workflows/ci.yml/badge.svg)](https://github.com/rndazurescript/Coco2CustomVision/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/release/rndazurescript/Coco2CustomVision/all.svg)](https://github.com/rndazurescript/Coco2CustomVision/releases)

A simple utility to upload a [COCO dataset](https://cocodataset.org/) format to custom vision and vice versa. This can be used to backup your custom vision object detection projects into a storage account and restore it later or use AzureML to create a more custom CV model.

Currently the scripts work with Object Detection but can be easily updated to work with Classification.

## Installation

Install from pip:

```bash
pip install coco2customvision
```

## Usage

To export a custom vision project to an Azure storage account use the following:

```bash
coco2customvision export -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

To import a coco dataset that is located in an Azure storage account container into a custom vision project (the project may not exist yet):

```bash
coco2customvision import -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

You can get the parameters from:

- [Custom vision](https://www.customvision.ai/projects#/settings): custom_vision_key, custom_vision_endpoint, custom_vision_project_name
- [Azure portal](https://portal.azure.com/): storage_account_key, storage_account_name, storage_account_container_name

## Code development

If you want to contribute to this code base, clone the repo and follow these instructions.

### Development installation

Install module in [editable/develop mode](https://pip.pypa.io/en/stable/cli/pip_install/#install-editable) (`-e`) and include the development dependencies (the `[dev]` argument you see) using the following:

```bash
pip install -e .[dev]
```

For tests to complete, you need to configure some secrets. These secrets are retrieved from environment variables. To avoid adding these environment variables in your system, you need to create a `pytest.ini` file based on the `pytest.ini.template` template and fill in all needed values. Use the following links to retrieve the corresponding settings:

- [Custom vision](https://www.customvision.ai/projects#/settings)
- [Azure storage account](https://portal.azure.com/).

> The `pytest.ini` file is in `.gitignore` to avoid pushing credentials accidentally.

To run all tests:

```bash
python -m pytest . -c pytest.ini
```

or use the [VSCode Test Explorer](https://code.visualstudio.com/docs/python/testing) to even debug your code.

### [Optional] Invoking the dev code from command line

If you installed the module in develop mode you can use it directly as seen in the instructions above. You can also use the module reference, as seen bellow.

To export a custom vision project to an Azure storage account use the following:

```bash
python -m src.coco2customvision export -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

To import a coco dataset that is located in an Azure storage account container into a custom vision project (the project may not exist yet):

```bash
python -m src.coco2customvision import -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

### Code quality practices

Before making any commit you can invoke the `pre-commit.bat` file which does the following:

- Format the code using `black`:

  ```bash
  python -m black . 
  ```

- Ensure that there is no `flake8` error:

  ```bash
  python -m flake8 .
  ```

- Ensure all test pass:

  ```bash
  python -m pytest . -c pytest.ini
  ```

- Ensure `setup.cfg` file is [consistently formatted](https://github.com/asottile/setup-cfg-fmt):

  ```bash
  setup-cfg-fmt setup.cfg
  ```

### Publishing to pypi

To create a release you need to create an annotated tag:

```bash
git tag -a v0.1.0 -m "First version of the tool"
```

You can view existing tags and their comments (`-n`) using:

```bash
git tag -n
```

Run a build to create the corresponding version artifacts under the `dist` folder. Then push them to `testpypi` to verify:

```bash
pip install --upgrade twine
twine upload --repository testpypi dist/*
```

Verify results in the [test Pypi](https://test.pypi.org/project/coco2customvision/) instance. You can try installing in a new python environment using:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple coco2customvision
```

If you decide to make some more changes, you can delete a tag using the following:

```bash
git tag -d v0.1.0
```

> Note: You will not be able to push the same version to the test Pypi instance. As a work around you can increase the prerelease 4th digit e.g. 0.1.0.1.

When you are ready push changes to remote and let github actions publish the package to the production Pypi. Just push the tag to GitHub and the CD action will create the release:

```bash
git push origin --tags
```

> Note that currently the CD process is kicked when you push the tag and it doesn't do the CI part. So make sure your code is passing the CI part before tagging and pushing the tag to GitHub.

## References

Here is a list of related projects and references to this effort:

- [Custom vision blob connector](https://github.com/drcrook1/Azure_CustomVision_Blob_Connector) python tool to upload images to custom vision from blob storage.
- [CustomVision.COCO](https://github.com/vladkol/CustomVision.COCO) C# tool to train models using a COCO definition file.
- [VoTT2COCO](https://github.com/UAVVaste/VoTT2COCO) converts [VoTT](https://github.com/microsoft/VoTT) json files to COCO format.
- [Azure cognitive services python SDK](https://docs.microsoft.com/samples/azure-samples/cognitive-services-python-sdk-samples/cognitive-services-python-sdk-samples/)
- [Custom vision SDK](https://docs.microsoft.com/python/api/azure-cognitiveservices-vision-customvision/)
- [Description of the COCO format](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch)

List of Python related references:

- [Writing python in VSCode](https://code.visualstudio.com/docs/python/python-tutorial)
- [Fixtures in pytest](https://docs.pytest.org/en/latest/how-to/fixtures.html)
- [Click arguments parser](https://click.palletsprojects.com/)
- [Packaging projects](https://packaging.python.org/tutorials/packaging-projects/)
- [Dependency management](https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html)
- [Docs authoring pack](https://marketplace.visualstudio.com/items?itemName=docsmsft.docs-authoring-pack), highly recommended collection of VSCode plugins.
