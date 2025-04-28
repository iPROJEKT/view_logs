from direct.gui.DirectDialog import OkDialog


from direct.gui.DirectDialog import OkDialog
from panda3d.core import TextNode

class ErrorDialogsUI:
    def __init__(self, config, base, node=None, button=None):
        self.config = config
        self.base = base
        self.node = node
        self.button = button
        self.error_dialog = None

    def show_error_dialog(self, message):
        # Clean up any existing dialog
        self.cleanup()

        self.error_dialog = OkDialog(
            text=message,
            text_wordwrap=20,
            text_align=TextNode.ACenter,
            text_scale=0.06,
            text_pos=(0, 0.2),
            buttonTextList=["OK"],
            command=self._on_dialog_ok,
            parent=self.node if self.node else self.base.aspect2d,
            pos=(0, 0, 0),  # Center the dialog
            scale=1.0
        )

        # Disable the button (if provided) while dialog is active
        if self.button:
            self.button['state'] = 'disabled'

    def _on_dialog_ok(self, value):
        # Clean up the dialog when OK is pressed
        self.cleanup()

    def cleanup(self):
        # Properly destroy the dialog if it exists
        if self.error_dialog:
            self.error_dialog.destroy()
            self.error_dialog = None
        # Re-enable the button (if provided)
        if self.button:
            self.button['state'] = 'normal'
