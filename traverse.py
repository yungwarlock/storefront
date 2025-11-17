from pathlib import Path
from typing import Tuple, Mapping

file = "/categories"
file = "/categories/1/products/1"
file = "/index"
file = "notexist"


def find_variables(request_path: str, root_dir: str) -> Tuple[str, Mapping[str, str]]:
    root_path = Path(root_dir)
    current_path = root_path
    path_variables = {}

    parts = request_path.strip("/").split("/")
    if parts == [""]:
        parts = []

    if not parts:  # Handle root path lookup
        index_file = root_path / "index.liquid"
        if index_file.is_file():
            return str(index_file), {}
        return "", {}

    for i, part in enumerate(parts):
        is_last_part = i == len(parts) - 1
        found_match_path = None

        try:
            child_paths = list(current_path.iterdir())
        except (NotADirectoryError, FileNotFoundError):
            return "", {}  # Current path is a file or does not exist

        # 1. Check for a static match
        static_match = current_path / part
        if static_match.is_dir():
            if is_last_part:
                index_file = static_match / "index.liquid"
                if index_file.is_file():
                    found_match_path = index_file
            else:
                found_match_path = static_match
        elif is_last_part:
            file_match = current_path / f"{part}.liquid"
            if file_match.is_file():
                found_match_path = file_match

        # 2. If no static match, check for a dynamic match
        if not found_match_path:
            for child in child_paths:
                if child.stem.startswith("[") and child.stem.endswith("]"):
                    var_name = child.stem.strip("[]")
                    if var_name not in path_variables:
                        path_variables[var_name] = part
                        found_match_path = child
                        break  # Take the first dynamic match

        if found_match_path:
            current_path = found_match_path
        else:
            return "", {}  # No match found for this part

    # After the loop, the final path must be a file
    if not current_path.is_file():
        return "", {}

    return str(current_path), path_variables


if __name__ == "__main__":
    print(find_variables(file, "examples"))
