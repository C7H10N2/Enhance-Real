import os
import subprocess

ALLOWED_EXTENSIONS = (".jpg", ".png")

def run_realesrgan(net, input_file, output_file):
    command = f"realesrgan-ncnn-vulkan.exe -g 0 -i {input_file} -o {output_file} -n {net}"
    process = subprocess.Popen(command, shell=True)
    return process

def filter_image_format(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".jpg" or ext == ".png":
        return file_path
    else:
        new_file_path = os.path.splitext(file_path)[0] + ".jpg"
        image = Image.open(file_path)
        image.save(new_file_path, "JPEG")
        return new_file_path
