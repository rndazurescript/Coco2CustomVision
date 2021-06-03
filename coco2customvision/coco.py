import logging
from datetime import date


log = logging.getLogger(__name__)

# The COCO bounding box format is [top left x position, top left y position, width, height].


def get_max_id(coco_section):
    max_id = max(coco_section, key=lambda x: x["id"])["id"] if coco_section else 0
    return max_id


def get_empty_coco_dataset(description="", url="", contributor=""):
    return {
        "info": {
            "description": description,
            "url": url,
            "version": "1.0",
            "year": date.today().year,
            "contributor": contributor,
            "date_created": date.today().strftime("%Y/%m/%d"),
        },
        "images": [],
        "annotations": [],
        "licenses": [
            {
                "id": 1,
                "name": "Attribution-NonCommercial-ShareAlike License",
                "url": "http: //creativecommons.org/licenses/by-nc-sa/2.0/",
            }
        ],
        "categories": [],
    }
