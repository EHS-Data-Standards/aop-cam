"""Data model package for aop-cap."""

from pathlib import Path
from .aop_cap import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "aop_cap.yaml"
