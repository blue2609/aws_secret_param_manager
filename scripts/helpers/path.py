import sys
from pathlib import Path


def add_root_dir_to_search_path():
    PROJ_ROOT_DIR = "secret-param-manager"
    PROJ_ROOT_DIR_FOUND = False

    parent_dir_path = Path(__file__).parent
    parent_dir_name = parent_dir_path.stem

    while not PROJ_ROOT_DIR_FOUND:
        if parent_dir_name == PROJ_ROOT_DIR.lower():
            PROJ_ROOT_DIR_FOUND = True
        else:
            parent_dir_path = parent_dir_path.parent
            parent_dir_name = parent_dir_path.stem

    sys.path.append(str(parent_dir_path))
