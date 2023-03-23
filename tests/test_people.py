import pytest

from src.project.models import PageRefs, People
from src.project.utils.query_helper import get_record_by_name, get_record_by_page_name
from tests import params


class TestCharacters:
    @pytest.mark.parametrize(
        "id, endpoint, expected",
        params.characters_get_params,
        ids=params.characters_get_ids,
    )
    def test_get_characters(self, app, client, id, endpoint, expected):
        response = client.get(endpoint)
        assert response.status_code == expected

    def test_post_characters_new(self, app, clean_test_tables, client): 
        response = client.post("/characters/", json={"name": "mytestname", "page": 66, "role": "Test"})

        check = get_record_by_name(model=People, name="mytestname")
        check_page = get_record_by_page_name(model=PageRefs, name="mytestname", page=66)

        assert check
        assert check_page

    def test_post_characters_update(self, app, clean_test_tables, client): 
        response = client.post("/characters/", json={"name": "Martine", "page": 50, "role": "Murderer"})

        check = get_record_by_name(model=People, name="Martine")
        check_page = get_record_by_page_name(model=PageRefs, name="Martine", page=50)

        assert check.role == "Murderer"
        assert check_page.page == 50

    def test_get_no_records(self, app, client, empty_test_tables, clean_test_tables):
        response = client.get("/characters/")

        assert response.status_code == 200
        assert response.json.get('message') == "No records"
        
