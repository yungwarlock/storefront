import asyncio
from pathlib import Path
from functools import partial
from typing import Optional, Tuple, Mapping

from liquid import Environment
from liquid import RenderContext
from liquid.loader import BaseLoader
from liquid.loader import TemplateSource
from liquid.exceptions import TemplateNotFoundError

ext = ".liquid"
encoding = "utf-8"


class PathLoader(BaseLoader):
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
        if not source_path or not Path(source_path).exists:
            raise TemplateNotFoundError(source_path)

        source, mtime = self._read(source_path)

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
        root_path = Path(root)
        current_path = root_path
        path_variables = {}

        parts = file.strip("/").split("/")
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
                        # Keep the "_id" suffix convention from the original loader
                        if (var_name + "_id") not in path_variables:
                            path_variables[var_name + "_id"] = part
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
