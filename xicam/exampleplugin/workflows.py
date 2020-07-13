"""Defines an example workflow to use in the ExamplePlugin."""
from xicam.core.execution import Workflow

from .operations import invert, random_noise, fft


class ExampleWorkflow(Workflow):
    """Example workflow that contains two operations: invert and random_noise"""
    def __init__(self):
        super(ExampleWorkflow, self).__init__(name="Example Workflow")

        # Create instances of our operations
        invert_op = invert()
        random_noise_op = random_noise()
        fft_op = fft()
        # Add our operations to the workflow
        self.add_operations(invert_op, random_noise_op, fft_op)
        # Connect invert's "output_image" value to random_noises "image" input argument
        self.add_link(invert_op, random_noise_op, "output_image", "image")
        self.add_link(random_noise_op, fft_op, "output_image", "image")
        self._pretty_print()  # Optional - prints out the workflow visually to the console






