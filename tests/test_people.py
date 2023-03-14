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

    def test_post_characters_new(
        self, app, clean_test_tables, client, people_form_test_data
    ):
        form = people_form_test_data.get("new")
        response = client.post("/characters/", data=form.data, follow_redirects=True)

        check = get_record_by_name(model=People, name="Test name")
        check_page = get_record_by_page_name(model=PageRefs, name="Test name", page=66)

        assert check

    def test_post_characters_update(
        self, app, clean_test_tables, client, people_form_test_data
    ):
        form = people_form_test_data.get("update")
        response = client.post("/characters/", data=form.data, follow_redirects=True)

        check = get_record_by_name(model=People, name="Martine")
        check_page = get_record_by_page_name(model=PageRefs, name="Martine", page=50)

        assert check.role == "Murderer"
        assert check_page.page == 50

    def test_get_no_records(self, app, client, empty_test_tables, clean_test_tables):
        response = client.get("/characters/")

        assert response.status_code == 200
        assert "No records" in response.text
