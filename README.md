# Coco2CustomVision
A simple utility to upload a [COCO dataset](https://cocodataset.org/) format to custom vision and vice versa. This can be used to backup your custom vision object detection projects into a storage account and restore it later or use AzureML to create a more custom CV model.

Currently the scripts work with Object Detection but can be easily updated to work with Classification. 

## Installation

Install from pip

```
pip install coco2customvision
```

## Usage

To export a custom vision project to an Azure storage account use the following:
```
coco2customvision export -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

To import a coco dataset that is located in an Azure storage account container into a custom vision project (the project may not exist yet):
```
coco2customvision import -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

You can get the parameters from:
- [Custom vision](https://www.customvision.ai/projects#/settings): custom_vision_key, custom_vision_endpoint, custom_vision_project_name
- [Azure portal](https://portal.azure.com/): storage_account_key, storage_account_name, storage_account_container_name


## Code development

If you want to contribute to this code base, clone the repo and follow these instructions.

### Development installation

Install all dependencies using:

```
pip install -r requirements.txt
```

For tests to complete, you need to either configure the environment variables defined in  the `pytest.ini.template` file or create a `pytest.ini` file from the template, filling in all secrets to your [Custom vision](https://www.customvision.ai/projects#/settings) and [Azure storage account](https://portal.azure.com/). This file is `.gitignored` to avoid pushing credentials accidentally.

To run all tests:
```
python -m pytest . -c pytest.ini
```

### Invoking the dev code from command line

To export a custom vision project to an Azure storage account use the following:
```
python -m coco2customvision export -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

To import a coco dataset that is located in an Azure storage account container into a custom vision project (the project may not exist yet):
```
python -m coco2customvision import -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```

### Code quality practises

Before making any commit:

- Format the code using `black`:
  ```
  python -m black . 
  ```
- Ensure that there is no `flake8` error:
  ```
  python -m flake8 .
  ```
- Ensure all test pass:
  ```
  python -m pytest . -c pytest.ini
  ```
- Ensure `setup.cfg` file is [consistently formatted](https://github.com/asottile/setup-cfg-fmt):
  ```
  setup-cfg-fmt setup.cfg
  ```

## References

Here is a list of related projects and references to this effort:

- [Custom vision blob connector](https://github.com/drcrook1/Azure_CustomVision_Blob_Connector) python tool to upload images to custom vision from blob storage.
- [CustomVision.COCO](https://github.com/vladkol/CustomVision.COCO) C# tool to train models using a COCO definition file.
- [VoTT2COCO](https://github.com/UAVVaste/VoTT2COCO) converts [VoTT](https://github.com/microsoft/VoTT) json files to COCO format.
- [Azure cognitive services python SDKs](https://docs.microsoft.com/en-us/samples/azure-samples/cognitive-services-python-sdk-samples/cognitive-services-python-sdk-samples/)
- [Custom vision SDK](https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-customvision/)
- [Description of the COCO format](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch)

List of Python related refences:
- [Fixtures in pytest](https://docs.pytest.org/en/latest/how-to/fixtures.html)
- [Click arguments parser](https://click.palletsprojects.com/)
- [Packaging projects](https://packaging.python.org/tutorials/packaging-projects/)