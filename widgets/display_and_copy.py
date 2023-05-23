import ipywidgets as widgets
import pyperclip
from IPython.display import display
import threading
import time


# Displaying text in a widget and copying it to the clipboard
def display_and_copy(text):
    output_text = widgets.Text()
    output_text.value = text

    def on_copy_button_click(button):
        copy_to_clipboard(text, button)

    copy_button = widgets.Button(description="Copy", button_style="primary")
    copy_button.on_click(on_copy_button_click)
    vbox = widgets.VBox([output_text, copy_button])
    display(vbox)

# Helper functions
def copy_to_clipboard(text, button):
    pyperclip.copy(text)
    button.button_style = "success"
    button.description = "Copied!"

    # Create a new thread to update the button style
    t = threading.Thread(target=update_button_style, args=(button,))
    t.start()


def update_button_style(button):
    # Wait for 2 seconds
    time.sleep(2)

    # Update button style
    button.button_style = "primary"
    button.description = "Copy"
