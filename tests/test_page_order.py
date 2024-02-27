import pytest

from src.project.forms import PageOrderForm
from src.project.models import PageOrder
from src.project.utils.query_helper import get_record_by_page_order



# @pytest.fixture(scope="function")
# def page_order_test_data():
#     data = get_form_data("page_order_form_data")
#     return {k: PageOrderForm(data=v) for k, v in data.items()}


# class TestPageOrder:
#     def test_get_page_order(self, app, client):
#         response = client.get("/page-order/")
#         assert response.status_code == 200

#     def test_post_page_order_new(
#         self, app, client, clean_test_tables, page_order_test_data
#     ):
#         form = page_order_test_data.get("new")
#         client.post("/page-order/", data=form.data, follow_redirects=True)

#         check = get_record_by_page_order(model=PageOrder, order=22, page=43)
#         assert check

#     def test_post_page_order_update(
#         self, app, client, clean_test_tables, page_order_test_data
#     ):
#         form = page_order_test_data.get("update")
#         client.post("/page-order/", data=form.data, follow_redirects=True)

#         check = get_record_by_page_order(model=PageOrder, order=71, page=3)
#         assert check

#     def test_post_page_order_no_update(self, app, client, clean_test_tables, caplog):
#         form_data = {"id": 1, "page": 20, "order": 81}
#         client.post("/page-order/", data=form_data, follow_redirects=True)
#         assert "Not updating" in caplog.text
