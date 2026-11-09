"""Validate example data against the aop_cam schema."""
import glob
import os
from pathlib import Path

import pytest
from linkml_runtime.loaders import yaml_loader

import aop_cam.datamodel.aop_cam as dm

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"

VALID_EXAMPLE_FILES = sorted(glob.glob(os.path.join(DATA_DIR_VALID, "*.yaml")))
INVALID_EXAMPLE_FILES = sorted(glob.glob(os.path.join(DATA_DIR_INVALID, "*.yaml")))


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath):
    """Every file in tests/data/valid loads against the tree root."""
    obj = yaml_loader.load(filepath, target_class=dm.ModelCollection)
    assert obj


@pytest.mark.parametrize("filepath", INVALID_EXAMPLE_FILES)
def test_invalid_data_files(filepath):
    """Every file in tests/data/invalid fails to load against the tree root."""
    with pytest.raises(Exception):
        yaml_loader.load(filepath, target_class=dm.ModelCollection)
