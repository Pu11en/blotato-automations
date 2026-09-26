"""Catalog type system for blotato-studio.

Ported from the open-higgsfield architecture (github.com/wide-trace/open-higgsfield):
a small declarative ModelEntry per technique, plus a generic GenerationPlane
that any entry's build_inputs() turns into the real Blotato request body.
Adding a new technique is one small file, not a new script.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Literal, Optional

Surface = Literal["image", "video"]
MediaRole = Literal["reference", "start", "end"]


@dataclass(frozen=True)
class SettingField:
    kind: Literal["enum", "range", "boolean", "text"]
    default: object
    values: Optional[tuple] = None
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None


@dataclass(frozen=True)
class MediaItem:
    asset_id: str
    url: str
    caption: Optional[str] = None


@dataclass
class GenerationPlane:
    """The generic, model-agnostic description of one generation request."""
    model_id: str
    prompt: str
    media: dict  # MediaRole -> list[MediaItem]
    settings: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ModelEntry:
    id: str
    blotato_template_id: str
    surface: Surface
    label: str
    description: str
    roles: dict  # MediaRole -> (min_count, max_count)
    settings: dict  # setting name -> SettingField
    build_inputs: Callable[[GenerationPlane], dict]
    known_issues: tuple = ()
    broken: bool = False
    verified_at: Optional[str] = None
    prompt_min_length: Optional[int] = None
    prompt_max_length: Optional[int] = None
    # Credits a live run actually cost us, not a published price list.
    observed_credits: Optional[float] = None
    # Set when one number cannot describe the cost (e.g. free with uploaded
    # media, charged per generated scene).
    cost_note: Optional[str] = None
    # Which package contributed this entry; the registry fills it in.
    origin: str = "blotato"

    @property
    def is_known_broken(self) -> bool:
        return self.broken

    def with_origin(self, origin: str) -> "ModelEntry":
        return self if self.origin == origin else replace(self, origin=origin)
