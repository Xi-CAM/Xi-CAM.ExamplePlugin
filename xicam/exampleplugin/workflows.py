from xicam.core.execution import Workflow

from .operations import invert, random_noise


class ExampleWorkflow(Workflow):

    def __init__(self):
        super(ExampleWorkflow, self).__init__(name="Example Workflow")

        invert_op = invert()
        random_noise_op = random_noise()
        self.add_operations(invert_op, random_noise_op)
        self.add_link(invert_op, random_noise_op, "output_image", "image")
        self._pretty_print()






