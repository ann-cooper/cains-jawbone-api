import json

import pytest

from src.project.models import PageRefs, People
from src.project.utils.extract_fields import DataToModelMapper


@pytest.fixture(scope="function")
def people_page_refs_data():
    with open("tests/demo_data.json", "r") as f:
        data = json.load(f)
    return data.get("people_form_data")


@pytest.fixture(scope="function")
def data_to_model_mapper(people_page_refs_data):
    mapper = DataToModelMapper(
        models=[People, PageRefs], form_data=people_page_refs_data
    )

    return mapper


@pytest.fixture(scope="function")
def mapper_with_keys(data_to_model_mapper):
    return data_to_model_mapper.extract_db_fields()


def test_extract_db_fields(data_to_model_mapper):
    fields = data_to_model_mapper.extract_db_fields()
    expected = {
        "People": ["id", "name", "role"],
        "PageRefs": ["id", "page", "people_id", "name"],
    }
    assert fields.keys_dict == expected


def test_form_unpack(mapper_with_keys):
    results = mapper_with_keys.form_unpack()
    expected = {
        "PageRefs": {"id": None, "name": "Test name", "page": 66, "people_id": None},
        "People": {"id": None, "name": "Test name", "role": "Test role"},
    }
    assert results.new_objs == expected


def test_pg_data_load():
    data = {"id": 4, "name": "Martine", "role": "Unknown"}
    result = DataToModelMapper.pg_data_load(People, data)
    assert result.name == "Martine"
