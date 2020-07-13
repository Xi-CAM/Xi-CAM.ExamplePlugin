# Here is a quick example plugin that uses Xi-CAM's CatalogView mixin
# to open and display a catalog from the "example_catalog".
from qtpy.QtWidgets import QSlider, QVBoxLayout, QLabel, QWidget
from qtpy.QtCore import Qt
# qtpy -> PySide 2 -->  Qt (C++)
#      -> PyQt5  -->
from xicam.plugins import GUILayout, GUIPlugin
from xicam.gui.widgets.dynimageview import DynImageView
from xicam.gui.widgets.imageviewmixins import CatalogView
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor

from .workflows import ExampleWorkflow


from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from xicam.plugins import OperationPlugin
class DBGWidget(QWidget):
    def __init__(self, parent=None, op: OperationPlugin = None):
        super(DBGWidget, self).__init__(parent)
        self.op = op  # OperationPlugin
        toggleFix = QPushButton("toggle fix")
        changeValue = QPushButton("change value")
        toggleFix.clicked.connect(self._toggle_fix)
        changeValue.clicked.connect(self._update_value)
        layout = QHBoxLayout()
        layout.addWidget(toggleFix)
        layout.addWidget(changeValue)
        self.setLayout(layout)
    def _toggle_fix(self, _):
        print(f"op fixed: {self.op.fixed}")
        key = "strength"
        self.op.fixed[key] = not self.op.fixed[key]
    def _update_value(self, _):
        print(f"op {self.op.name} change value: {self.op.filled_values}")
        key = "strength"
        value = 0.0
        if key not in self.op.filled_values:
            value = 0.5
        else:
            value = self.op.filled_values[key]
        self.op.filled_values[key] = value + 0.1
        #     c = self.op.filled_values.copy()
        #     v = c["strength"] + 0.1
        #     c.update({"strength": v})
        #     self.op.filled_values = c
        # if key in self.op.filled_values:
        #     strength = self.op.filled_values[key]
        #     if strength >= 1.0:
        #         strength = 0.0
        #     else:
        #         strength += 0.1
        #     filled_values = self.op.filled_values.copy()
        #     filled_values[key] = strength
        #     self.op.filled_values = 3

class ExamplePlugin(GUIPlugin):
    """Derived GUIPlugin class to define our own GUIPlugin called ExamplePlugin"""
    # Define the name of the plugin (how it is displayed in Xi-CAM)
    name = "Example Plugin"

    def __init__(self, *args, **kwargs):
        """Constructs the ExamplePlugin

        This will set up the widgets that we want the ExamplePlugin to have,
        the layout for the widgets (how the interface will look) in the ExamplePlugin,
        and an example workflow.
        """
        self._catalog_viewer = CatalogView()  # Create a widget to view the loaded catalog
        self._results_viewer = DynImageView()  # Create a widget to view the result image

        self._workflow = ExampleWorkflow()  # Create a workflow
        # Create a widget for the workflow; this shows the operations and their paramters,
        # and we can run the workflow with this widget
        self._workflow_editor = WorkflowEditor(workflow=self._workflow)
        # The WorkflowEditor emits a "sigRunWorkflow" signal when its "Run Workflow" is clicked
        # This will call our run_workflow method whenever this signal is emitted (whenever the button is clicked).
        self._workflow_editor.sigRunWorkflow.connect(self.run_workflow)

        # Create a layout to organize our widgets
        # The first argument (which corresponds to the center widget) is required.
        # ops = self._workflow.operations
        #
        # self.slider_widget = QWidget()
        #
        # self.slider = QSlider(orientation=Qt.Horizontal)
        # self.slider.setMinimum(0)
        # self.slider.setMaximum(12)
        # self.slider.setTickInterval(3)
        #
        # self.slider.valueChanged.connect(self.slider_update)
        # self.slider.valueChanged.connect(self.mult_image)
        #
        # self.label = QLabel("placeholder")
        #
        # layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # layout.addWidget(self.slider)
        # self.slider_widget.setLayout(layout)

        catalog_viewer_layout = GUILayout(self._catalog_viewer,
                                          right=self._workflow_editor,
                                          bottom=self._results_viewer)
                                          # rightbottom=DBGWidget(op=ops[-1]),
                                          # righttop=self.slider_widget)

        # Create a "View" stage that has the catalog viewer layout
        self.stages = {"View": catalog_viewer_layout}

        # For classes derived from GUIPlugin, this super __init__ must occur at end
        super(ExamplePlugin, self).__init__(*args, **kwargs)

    # def mult_image(self, value):
    #     self._results_viewer.setImage(self.output_image * value)
    #
    # def slider_update(self, value):
    #     self.label.setText(str(value))
    #     print(value)

    def appendCatalog(self, catalog, **kwargs):
        """Re-implemented from GUIPlugin - gives us access to a catalog reference

        You MUST implement this method if you want to load catalog data into your GUIPlugin.
        """
        # Set the catalog viewer's catalog, stream, and field (so it knows what to display)
        # This is a quick and simple demonstration; stream and field should NOT be hardcoded
        stream = "primary"
        field = "img"
        self._catalog_viewer.setCatalog(catalog, stream, field)

    def run_workflow(self):
        """Run the internal workflow.

        In this example, this will be called whenever the "Run Workflow" in the WorkflowEditor is clicked.
        """
        if not self._catalog_viewer.catalog:  # Don't run if there is no data loaded in
            return
        # Use Workflow's execute method to run the workflow.
        # our callback_slot will be called when the workflow has executed its operations
        # image is an additional keyword-argument that is fed into the first operation in the workflow
        # (the invert operation needs an "image" argument)
        self._workflow.execute(callback_slot=self.results_ready,
                               image=self._catalog_viewer.image)
        #invert(image)

    def results_ready(self, *results):
        """Update the results view widget with the processed data.

        This is called when the workflow's execute method has finished running is operations.
        """
        # print(results)
        # results is a tuple that will look like:
        # ({"output_name": output_value"}, ...)
        # This will only contain more than one dictionary if using Workflow.execute_all
        output_image = results[0]["output_image"]  # We want the output_image from the last operation
        self.output_image = output_image
        self._results_viewer.setImage(output_image)# * self.slider.value())  # Update the result view widget


