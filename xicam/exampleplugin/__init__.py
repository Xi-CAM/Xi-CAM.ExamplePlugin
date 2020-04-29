from qtpy.QtWidgets import QLabel

from xicam.plugins import GUILayout, GUIPlugin


class ExamplePlugin(GUIPlugin):
    # Define the name of the plugin (how it is displayed in Xi-CAM)
    name = "Example Plugin"

    def __init__(self, *args, **kwargs):
        # Insert code here

        # Modify stages here
        self.stages = {"Stage 1": GUILayout(QLabel("Stage 1..."))}

        super(ExamplePlugin, self).__init__(*args, **kwargs)
