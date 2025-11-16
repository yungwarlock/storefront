import os
from pathlib import Path

file = "categories/1/products/1"
file = "index"


def find_variables(file: str, root: str):
    parts = file.split("/")
    count = len(parts)

    current_path = root
    for part in parts:
        count -= 1

        if count == 0:
            part = part + ".liquid"

        finding_path = current_path + "/" + part
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
            for file in folder_files:
                if file.find("["):
                    current_path = file

        if count == 0:
            return current_path


if __name__ == "__main__":
    print(find_variables(file, "storefront/examples"))
