from src.project.models import ReferenceInfo
from src.project.utils.query_helper import get_record_by_page_clue


class TestRefInfo:
    def test_get_ref_info(self, app, client):
        response = client.get("/reference-info/")
        assert response.status_code == 200

    def test_post_page_order_new(
        self, app, client, clean_test_tables, reference_info_form_test_data, caplog
    ):
        form = reference_info_form_test_data.get("new")
        client.post("/reference-info/", data=form.data, follow_redirects=True)

        check = get_record_by_page_clue(model=ReferenceInfo, page=10, clue="Test clue")
        assert check
        assert "Creating new" in caplog.text

    def test_post_ref_info_update(
        self, app, client, clean_test_tables, reference_info_form_test_data, caplog
    ):
        form = reference_info_form_test_data.get("update")
        client.post("/reference-info/", data=form.data, follow_redirects=True)

        check = get_record_by_page_clue(
            model=ReferenceInfo, page=71, clue="Spartan mother"
        )
        assert check.link == "updated.link.here"
        assert "Will update" in caplog.text
