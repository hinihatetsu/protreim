from PIL import Image
from typing import Tuple, Callable, Union

Color = Union[str, Tuple[int, int, int]]
ProcessFunc = Callable[[Image.Image], Image.Image]