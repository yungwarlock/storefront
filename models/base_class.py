import inspect
from collections import abc
from pydantic import BaseModel
from typing import Any, Iterator, Set
from functools import cached_property


class LiquidDropModel(BaseModel, abc.Mapping[str, Any]):
    """
    A Pydantic BaseModel that also works as a Liquid 'drop'.

    It automatically exposes all Pydantic fields and any
    methods decorated with @property to Liquid templates.
    """

    @cached_property
    def _liquid_keys(self) -> Set[str]:
        """
        Automatically finds and caches all keys to be exposed to Liquid.

        This includes all Pydantic fields and all @property methods.
        Subclasses can override this for more complex logic.
        """
        # 1. Get all Pydantic model fields
        model_fields = set(self.model_fields.keys())

        # 2. Get all @property methods
        properties = set()
        for name, _ in inspect.getmembers(
            self.__class__, lambda o: isinstance(o, property)
        ):
            # Exclude internal/private properties
            if not name.startswith("_"):
                properties.add(name)

        return model_fields.union(properties)

    # --- abc.Mapping Implementation ---

    def __getitem__(self, key: str) -> Any:
        """Called when Liquid tries to access a key like {{ model.key }}."""
        if key in self._liquid_keys:
            return getattr(self, key)

        # This is required for Liquid to know the key doesn't exist
        raise KeyError(f"Key '{key}' is not a valid liquid drop key")

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Returns an iterator of all available keys."""
        return iter(self._liquid_keys)

    def __len__(self) -> int:
        """Returns the count of all available keys."""
        return len(self._liquid_keys)
