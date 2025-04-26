from direct.gui.DirectDialog import OkDialog


class ErrorDialogsUI:
    def __init__(self, config, base, **kwargs):
        self.config = config
        self.base = base
        self.node = kwargs.get("node", None)
        self.button = kwargs.get("button", None)
        self.custom_font = self.base.loader.loadFont(self.config.custom_font)
        self.error_dialog = None

    def show_error_dialog(self, message):
        """Show an error dialog with the specified message."""
        # Destroy any existing dialog
        if self.error_dialog:
            self.error_dialog.destroy()
            self.error_dialog = None

        # Use a unique dialog name to avoid conflicts
        unique_name = f"ErrorDialog_{id(self)}"
        self.error_dialog = OkDialog(
            dialogName=unique_name,
            text=message,
            buttonTextList=["OK"],
            command=self.close_error_dialog,
            text_font=self.custom_font,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_dialog.show()
        if self.button:
            self.button.hide()
        if self.node:
            self.node.hide()

    def close_error_dialog(self, _):
        """Close the error dialog."""
        if self.error_dialog:
            self.error_dialog.hide()
            if self.button:
                self.button.show()
            if self.node:
                self.node.show()
