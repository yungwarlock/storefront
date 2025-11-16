import os
import re
from pathlib import Path
from typing import Tuple, Mapping

file = "categories/1/products/1"
file = "index"
file = "notexist"


def find_variables(file: str, root: str) -> Tuple[str, Mapping[str, str]]:
    parts = file.split("/")
    count = len(parts)

    path_variables = {}

    current_path = root
    for part in parts:
        count -= 1

        finding_path = current_path + "/" + part
        if count == 0:
            finding_path = finding_path + ".liquid"
        folder_files = list(
            map(
                lambda x, current_path=current_path: current_path + "/" + x,
                os.listdir(current_path),
            )
        )

        # Check direct match
        if finding_path in folder_files:
            if count == 0:
                if Path(finding_path).is_file():
                    current_path = finding_path
            else:
                if Path(finding_path).is_dir():
                    current_path = finding_path
        # Check variable path
        else:
            for match_file in folder_files:
                matches = re.findall(r"\[(.*?)\]", match_file)
                if matches:
                    for match in matches:
                        if path_variables.get(match):
                            continue
                        path_variables[match] = part
                    current_path = match_file
                    break

    if current_path == root:
        return "", {}
    return current_path, path_variables


if __name__ == "__main__":
    print(find_variables(file, "storefront/examples"))
