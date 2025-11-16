import os
import re
import asyncio
from pathlib import Path
from typing import Optional
from functools import partial

from liquid import Environment
from liquid import RenderContext
from liquid.loader import BaseLoader
from liquid.loader import TemplateSource
from liquid.exceptions import TemplateNotFoundError

ext = ".liquid"
encoding = "utf-8"


class FileSystemLoader(BaseLoader):
    """A loader that loads templates from one or more directories on the file system.

    Args:
        search_path: One or more paths to search.
        encoding: Encoding to use when opening files.
        ext: A default file extension. Should include a leading period.
    """

    def __init__(
        self,
        path: str,
    ):
        super().__init__()

        self.path = Path(path)

    def resolve_path(self, template_name: str) -> Path:
        """Return a path to the template identified by _template_name_.

        If the search path is a list of paths, returns the first path where
        _template_name_ exists. If none of the search paths contain _template_name_, a
        _TemplateNotFound_ exception is raised.
        """
        template_path = Path(template_name)

        if ext and not template_path.suffix:
            template_path = template_path.with_suffix(ext)

        if os.path.pardir in template_path.parts:
            raise TemplateNotFoundError(template_name)

        source_path = self.path.joinpath(template_path)
        if not source_path.exists():
            raise TemplateNotFoundError(template_name)
        return source_path

    def _read(self, source_path: Path) -> tuple[str, float]:
        with source_path.open(encoding=encoding) as fd:
            source = fd.read()
        return source, source_path.stat().st_mtime

    def get_source(
        self,
        env: Environment,  # noqa: ARG002
        template_name: str,
        *,
        context: Optional[RenderContext] = None,  # noqa: ARG002
        **kwargs: object,  # noqa: ARG002
    ) -> TemplateSource:
        """Get source information for a template."""

        source_path = self.resolve_path(template_name)
        source, mtime = self._read(source_path)

        matter = {}

        match = re.search(r"[]", template_name)

        print("match_name", match)

        return TemplateSource(
            source,
            str(source_path),
            partial(self._uptodate, source_path, mtime),
            matter={
                "params": "1",
            },
        )

    @staticmethod
    def _uptodate(source_path: Path, mtime: float) -> bool:
        return mtime == source_path.stat().st_mtime

    @staticmethod
    async def _uptodate_async(source_path: Path, mtime: float) -> bool:
        return await asyncio.get_running_loop().run_in_executor(
            None, lambda: mtime == source_path.stat().st_mtime
        )

    async def get_source_async(
        self,
        env: Environment,  # noqa: ARG002
        template_name: str,
        *,
        context: Optional[RenderContext] = None,  # noqa: ARG002
        **kwargs: object,  # noqa: ARG002
    ) -> TemplateSource:
        """Get source information for a template."""
        loop = asyncio.get_running_loop()
        source_path = await loop.run_in_executor(None, self.resolve_path, template_name)
        source, mtime = await loop.run_in_executor(None, self._read, source_path)
        return TemplateSource(
            source, str(source_path), partial(self._uptodate_async, source_path, mtime)
        )
