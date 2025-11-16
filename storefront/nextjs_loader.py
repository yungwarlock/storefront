import os
import re
import asyncio
from pathlib import Path
from typing import Optional, Tuple, Mapping
from functools import partial

from liquid import Environment
from liquid import RenderContext
from liquid.loader import BaseLoader
from liquid.loader import TemplateSource
from liquid.exceptions import TemplateNotFoundError

ext = ".liquid"
encoding = "utf-8"


class FileSystemLoader(BaseLoader):
    def __init__(self, path: str):
        super().__init__()

        self.path = path

    def get_source(
        self,
        env: Environment,  # noqa: ARG002
        template_name: str,
        *,
        context: Optional[RenderContext] = None,  # noqa: ARG002
        **kwargs: object,  # noqa: ARG002
    ) -> TemplateSource:
        """Get source information for a template."""

        source_path, vars = self.get_effective_path(template_name, self.path)
        source, mtime = self._read(source_path)

        if not source_path:
            raise TemplateNotFoundError(template_name)

        return TemplateSource(
            source,
            str(source_path),
            partial(self._uptodate, Path(source_path), mtime),
            matter=vars,  # type: ignore
        )

    def _read(self, source_path: str) -> tuple[str, float]:
        with Path(source_path).open(encoding=encoding) as fd:
            source = fd.read()
        return source, Path(source_path).stat().st_mtime

    @staticmethod
    def _uptodate(source_path: Path, mtime: float) -> bool:
        return mtime == source_path.stat().st_mtime

    @staticmethod
    async def _uptodate_async(source_path: Path, mtime: float) -> bool:
        return await asyncio.get_running_loop().run_in_executor(
            None, lambda: mtime == source_path.stat().st_mtime
        )

    def get_effective_path(self, file: str, root: str) -> Tuple[str, Mapping[str, str]]:
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

            else:
                for match_file in folder_files:
                    matches = re.findall(r"\[(.*?)\]", match_file)
                    if matches:
                        for match in matches:
                            if path_variables.get(match + "_id"):
                                continue
                            path_variables[match + "_id"] = part
                        current_path = match_file
                        break

        if current_path == root:
            return "", {}
        return current_path, path_variables
