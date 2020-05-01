import numpy as np

from xicam.plugins.operationplugin import limits, operation, opts, output_names, visible


@operation
@output_names("output_image")
@visible("image", is_visible=False)
def invert(image: np.ndarray, x=1) -> np.ndarray:
    if issubclass(image.dtype.type, np.integer):
        max_value = np.iinfo(image.dtype).max
    else:
        max_value = np.finfo(image.dtype).max
    return max_value - image


@operation
@output_names("output_image")
@limits("strength", [0.0, 1.0])
@opts("strength", step=0.1)
@visible("image", is_visible=False)
def random_noise(image: np.ndarray, strength: float = 0.5) -> np.ndarray:
    if issubclass(image.dtype.type, np.integer):
        max_value = np.iinfo(image.dtype).max
    else:
        max_value = np.finfo(image.dtype).max
    return np.random.rand(*image.shape) * (strength * max_value) + image