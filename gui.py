import os
from PIL import Image, ImageTk
import PySimpleGUI as sg
from realesrgan import run_realesrgan, filter_image_format

def create_gui():
    left_layout = [
        [sg.Text("Please select the model:")],
        [sg.Radio("realesrgan-x4plus", "model", default=True, key="-MODEL1-")],
        [sg.Radio("reaesrnet-x4plus", "model", key="-MODEL2-")],
        [sg.Radio("realesrgan-x4plus-anime", "model", key="-MODEL3-")],
        [sg.Text("Please select the input image file:")],
        [sg.Input(key="-INPUT-", enable_events=True, visible=False),
         sg.FileBrowse(file_types=(("Image Files", "*.jpg;*.png"),))],
        [sg.Text("Please select the output image folder:")],
        [sg.Input(key="-OUTPUT-", size=(15,1)), sg.FolderBrowse()],
        [sg.Button("Run")]
    ]

    input_image_layout = [
        [sg.Text("Input Image", justification="center")],
        [sg.Image(key="-INPUT_IMAGE-", size=(200, 200))]
    ]

    layout = [
        [
            sg.Column(left_layout, element_justification="left", pad=(20, 20)),
            sg.Column(input_image_layout, element_justification="center")
        ]
    ]

    window = sg.Window("Real-ESRGAN", layout)

    running_process = None
    preview_input_image = None

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            if running_process and running_process.poll() is None:
                running_process.terminate()
                running_process.wait()
            break

        if event == "Run":
            net = ""
            if values["-MODEL1-"]:
                net = "realesrgan-x4plus"
            elif values["-MODEL2-"]:
                net = "reaesrnet-x4plus"
            elif values["-MODEL3-"]:
                net = "realesrgan-x4plus-anime"
            else:
                sg.popup("Please select the model!")
                continue

            input_file = values["-INPUT-"]
            output_folder = values["-OUTPUT-"]

            if not input_file:
                sg.popup("Please select the input image file!")
                continue

            if not output_folder:
                sg.popup("Please select the output image folder!")
                continue

            input_file_filtered = filter_image_format(input_file)
            input_filename = os.path.splitext(os.path.basename(input_file_filtered))[0]
            output_filename = f"{input_filename}x4.png"
            output_file = os.path.join(output_folder, output_filename)

            if running_process and running_process.poll() is None:
                sg.popup("A process is running, please wait for the current process to complete.")
                continue

            running_process = run_realesrgan(net, input_file_filtered, output_file)

        if event == "-INPUT-":
            if values["-INPUT-"]:
                try:
                    image = Image.open(values["-INPUT-"])
                    image.thumbnail((400, 400))
                    preview_input_image = image
                    window["-INPUT_IMAGE-"].update(data=ImageTk.PhotoImage(preview_input_image))
                except Exception as e:
                    sg.popup(f"Cannot open image files: {str(e)}")
            else:
                preview_input_image = None
                window["-INPUT_IMAGE-"].update(data=None)

    window.close()
