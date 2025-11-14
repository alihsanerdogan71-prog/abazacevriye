import os
import tempfile
from PIL import Image
import pytest
from db_utils import init_db_and_migrate, query_provinces, add_province, delete_province
from a4_utils import create_a4_from_label, mm_to_px

def test_db_migration_and_crud(tmp_path):
    # ensure DB created and seeded
    init_db_and_migrate()
    provs = query_provinces()
    assert isinstance(provs, list)
    # add a temp province
    add_province("TEST_PROVINCE_XYZ")
    provs2 = query_provinces("TEST_PROVINCE")
    assert "TEST_PROVINCE_XYZ" in provs2
    # cleanup
    delete_province("TEST_PROVINCE_XYZ")
    provs3 = query_provinces("TEST_PROVINCE")
    assert "TEST_PROVINCE_XYZ" not in provs3

def test_create_a4_single_and_tiled(tmp_path):
    # create a dummy label image 600x400 px
    label = Image.new("RGB", (600, 400), "white")
    # test single placement
    a4 = create_a4_from_label(label, margin_mm=10, rows=1, cols=1, dpi=203)
    assert a4.size[0] == mm_to_px(210, dpi=203)
    # save to temp for visual inspection if needed
    p1 = tmp_path / "a4_single.png"
    a4.save(str(p1))
    assert p1.exists()
    # test tiled 2x3
    a4_2 = create_a4_from_label(label, margin_mm=8, rows=2, cols=3, dpi=203)
    p2 = tmp_path / "a4_2x3.png"
    a4_2.save(str(p2))
    assert p2.exists()