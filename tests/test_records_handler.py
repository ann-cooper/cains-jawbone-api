import pytest

from src.project.utils.query_helper import find_model, get_record_by_id
from tests import params


class TestRecordsCleanup:
    def test_get_records_cleanup(self, app, client, clean_test_tables):
        response = client.get("/records-cleanup/")

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "id, type, expected", params.delete_post_params, ids=params.delete_ids
    )
    def test_post_records_cleanup(
        self, app, client, id, type, expected, delete_form_test_data, clean_test_tables
    ):
        form = delete_form_test_data.get(type)
        response = client.post(
            f"/records-cleanup/{type}", data=form.data, follow_redirects=True
        )
        model = find_model(type)
        check = get_record_by_id(model=model.get("model"), id=id)

        assert response.status_code == 200
        assert not check
