import os
import aws
from pathlib import Path
def startup():
    root_path=Path(aws.__file__).parent.parent
    logs_dir_path=os.path.join(root_path,"logs")
    if not os.path.isdir(logs_dir_path):
        os.mkdir(logs_dir_path)
startup()
