# Here is a quick example plugin that uses Xi-CAM's CatalogView mixin
# to open and display a catalog from the "example_catalog".

from xicam.plugins import GUILayout, GUIPlugin
from xicam.gui.widgets.dynimageview import DynImageView
from xicam.gui.widgets.imageviewmixins import CatalogView
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor

from .workflows import ExampleWorkflow


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
        catalog_viewer_layout = GUILayout(self._catalog_viewer,
                                          right=self._workflow_editor,
                                          bottom=self._results_viewer)

        # Create a "View" stage that has the catalog viewer layout
        self.stages = {"View": catalog_viewer_layout}

        # For classes derived from GUIPlugin, this super __init__ must occur at end
        super(ExamplePlugin, self).__init__(*args, **kwargs)

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

    def results_ready(self, *results):
        """Update the results view widget with the processed data.

        This is called when the workflow's execute method has finished running is operations.
        """
        # print(results)
        # results is a tuple that will look like:
        # ({"output_name": output_value"}, ...)
        # This will only contain more than one dictionary if using Workflow.execute_all
        output_image = results[0]["output_image"]  # We want the output_image from the last operation
        self._results_viewer.setImage(output_image)  # Update the result view widget


