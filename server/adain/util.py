import inspect
import os


def get_filename(path):
    return os.path.splitext(os.path.basename(path))[0]


def extract_image_names_recursive(top):
    img_exts = ['.jpg', '.jpeg', '.png']
    return [os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(top)
        for filename in filenames if os.path.splitext(filename)[1] in img_exts]


def get_params(fn):
    "Extract parameter names and their default values from a function"
    sig = inspect.signature(fn)
    empty = inspect.Parameter.empty
    return {name: param.default if param.default != empty else None
        for name, param in sig.parameters.items()}
