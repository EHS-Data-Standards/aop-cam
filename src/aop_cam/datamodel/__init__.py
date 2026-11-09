"""Data model package for aop-cam."""

from pathlib import Path
from .aop_cam import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "aop_cam.yaml"
