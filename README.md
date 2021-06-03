# Coco2CustomVision
A simple script to upload a [COCO dataset](https://cocodataset.org/) format to custom vision and vice versa.

Currently the scripts work with Object Detection but can be easily updated to work with Classification. 

## Accessing files in blob storage



## Installation

Install all dependencies using:

```
pip install -r requirements.txt
```

For tests to complete, add the following environment variables that you can get from https://www.customvision.ai/projects#/settings:
- CUSTOM_VISION_KEY
- CUSTOM_VISION_ENDPOINT

## Usage

To export a custom vision project to an Azure storage account use the following:
```
python -m coco2customvision export -sk "<storage_account_key>" -sn <storage_account_name> -sc <storage_account_container_name> -cvk <custom_vision_key> -cve <custom_vision_endpoint> -cvp <custom_vision_project_name> coco_dataset_filename.json
```
You can get the parameters from:
- [Custom vision](https://www.customvision.ai/projects#/settings): custom_vision_key, custom_vision_endpoint, custom_vision_project_name
- [Azure portal](https://portal.azure.com/): storage_account_key, storage_account_name, storage_account_container_name


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