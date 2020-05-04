# Here is a quick example plugin that uses Xi-CAM's CatalogView mixin
# to open and display a catalog from the "example-catalog".
from pyqtgraph.parametertree import ParameterTree
from pyqtgraph.parametertree.parameterTypes import ActionParameter, GroupParameter
from qtpy.QtWidgets import QVBoxLayout, QWidget

from xicam.plugins import GUILayout, GUIPlugin
from xicam.gui.widgets.imageviewmixins import CatalogView, XArrayView
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor

from .workflows import ExampleWorkflow

#
# class ParameterView(ParameterTree):
#
#     def __init__(self, workflow, button_clicked, parent=None):
#         super(ParameterView, self).__init__(parent)
#
#         for op in workflow.operations:
#             parameter = op.as_parameter()
#             group = GroupParameter(name=op.name, children=parameter)
#             self.addParameters(group)
#
#         run_workflow = ActionParameter(name="Run Workflow")
#         run_workflow.sigActivated.connect(button_clicked)
#         self.addParameters(run_workflow)
#         # self.setParameters(group)


class ExamplePlugin(GUIPlugin):
    # Define the name of the plugin (how it is displayed in Xi-CAM)
    name = "Example Plugin"

    def __init__(self, *args, **kwargs):

        self._catalog_viewer = CatalogView()  # Create a viewer for the loaded catalog
        self._results_viewer = XArrayView()

        # Create a workflow editor widget to modify parameters into the operations in our workflow
        self._workflow = ExampleWorkflow()
        self._workflow_editor = WorkflowEditor(workflow=self._workflow)
        self._workflow_editor.sigRunWorkflow.connect(self.run_workflow)

        # self._parameter_view = ParameterView(self._workflow,
        #                                      self.run_workflow)

        # Create a layout to organize our catalog viewer and workflow editor widgets
        # Our catalog viewer will show up in the middle, and our workflow on the right
        catalog_viewer_layout = GUILayout(self._catalog_viewer,
                                          right=self._workflow_editor,
                                          # righttop=self._parameter_view)
                                          bottom=self._results_viewer)

        # Create a "View" stage that has the catalog viewer layout
        self.stages = {"View": catalog_viewer_layout}

        # For classes derived from GUIPlugin, this super __init__ must occur at end
        super(ExamplePlugin, self).__init__(*args, **kwargs)

    def appendCatalog(self, catalog, **kwargs):
        # Re-implemented from GUIPlugin - gives us access to a catalog reference
        # Set the catalog viewer's catalog, stream, and field (so it knows what to display)
        # This is a quick and simple demonstration; stream and field should NOT be hardcoded
        stream = "primary"
        field = "img"
        self._catalog_viewer.setCatalog(catalog, stream, field)

    def run_workflow(self):
        if not self._catalog_viewer.catalog:
            return
        self._workflow.execute(image=self._catalog_viewer.xarray.dataarray,
                               callback_slot=self.results_ready)

    def results_ready(self, *results):
        print(results)
        output_image = results[0]["output_image"].values
        self._results_viewer.setImage(output_image)


