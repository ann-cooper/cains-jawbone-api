import pytest

from src.project.forms import PageRefForm
from src.project.models import PageRefs
from src.project.utils.query_helper import get_record_by_page_name


@pytest.fixture(scope="function")
def page_form_test_data(page_refs_form_data):
    return {k: PageRefForm(data=v) for k, v in page_refs_form_data.items()}


class TestPageInfo:
    def test_get_page_info(self, app, client):
        response = client.get("/page-info/")

        assert response.status_code == 200

    def test_post_page_info_new(
        self, app, client, clean_test_tables, page_form_test_data
    ):
        form = page_form_test_data.get("new")
        response = client.post("/page-info/", data=form.data, follow_redirects=True)
        check = get_record_by_page_name(model=PageRefs, name="Test name", page=100)

        assert check

    def test_post_info_update(
        self, app, client, clean_test_tables, page_form_test_data
    ):
        form = page_form_test_data.get("update")
        response = client.post("/page-info/", data=form.data, follow_redirects=True)
        check = get_record_by_page_name(model=PageRefs, name="Harry", page=10)

        assert check
