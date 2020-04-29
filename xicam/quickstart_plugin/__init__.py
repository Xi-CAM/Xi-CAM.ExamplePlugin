from qtpy.QtWidgets import QLabel

from xicam.plugins import GUILayout, GUIPlugin


class QuickStartPlugin(GUIPlugin):
    # Define the name of the plugin (how it is displayed in Xi-CAM)
    name = "QuickStart"

    def __init__(self, *args, **kwargs):
        # Insert code here

        # Modify stages here
        self.stages = {'Stage 1': GUILayout(QLabel("Stage 1..."))}

        super(QuickStartPlugin, self).__init__(*args, **kwargs)
