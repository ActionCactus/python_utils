from operations.operation import Operation
from PIL import Image
import logging

logger = logging.getLogger()

class AspectRatio(Operation):
    def __init__(self) -> None:
        self._payload = {
            "landscape": [],
            "portrait": []
        }
    def arg_name() -> str:
        return "aspect_ratio"

    @property
    def name(self) -> str:
        return "Filter-AspectRatio"

    def process_file(self, file_path: str):
        try:
            with Image.open(file_path) as image:
                w, h = image.size

                if w >= h:
                    self._payload["landscape"].append(file_path)
                else:
                    self._payload["portrait"].append(file_path)
        except Exception as e:
            logger.error(f"Could not gather exif for {file_path}")

    def gather_results(self):
        return self._payload

