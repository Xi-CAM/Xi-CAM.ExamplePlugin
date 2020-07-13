"""Simple example operations that are used to demonstrate some image processing in Xi-CAM.
"""
import numpy as np

from xicam.plugins.operationplugin import (limits, describe_input, describe_output, categories,
                                           operation, opts, output_names, visible, fixed, display_name)


# Define an operation that inverts the values of an image
@operation  # Required - defines the function below as an OperationPlugin
@output_names("output_image")  # Required - describes the names of the output(s)
@describe_input("image", "The image to invert")  # Optional - Description of an input argument
@describe_output("output_image", "The inverted image")  # Optional - Description of an output
@visible("image", is_visible=False)  # Optional - Prevents the input image arg from showing up in WorkflowEditor
def invert(image: np.ndarray) -> np.ndarray:
    if issubclass(image.dtype.type, np.integer):
        max_value = np.iinfo(image.dtype).max
    else:
        max_value = np.finfo(image.dtype).max
    return np.subtract(max_value, image)


# Define an operation that applies random noise to an image
@operation
@output_names("output_image")
@visible('image', False)
def random_noise(image: np.ndarray, strength: float = 0.5) -> np.ndarray:
    if issubclass(image.dtype.type, np.integer):
        max_value = np.iinfo(image.dtype).max
    else:
        max_value = np.finfo(image.dtype).max
    return (np.random.rand(*image.shape) * (strength * max_value) + image).astype(image.dtype)


@operation
@output_names("output_image")
def fft(image: np.ndarray) -> np.ndarray:

    return np.abs(np.fft.fftshift(np.fft.fft2(image)))
