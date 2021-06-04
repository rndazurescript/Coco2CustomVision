from io import StringIO
import json
from shutil import copyfileobj
from tqdm import tqdm


def serialize_to_stream(coco_dataset):
    content_io_buffer = StringIO()
    json.dump(coco_dataset, content_io_buffer, indent=4)
    return content_io_buffer


def stream_to_file(stream, filename):
    with open(filename, "w") as fd:
        stream.seek(0)
        copyfileobj(stream, fd)


def batch(iterable, n=1, message="Processing batch"):
    length = len(iterable)
    for ndx in tqdm(range(0, length, n), ascii=True, desc=message):
        yield iterable[ndx : min(ndx + n, length)]
