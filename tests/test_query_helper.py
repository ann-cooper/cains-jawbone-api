import pytest

from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.schemas import PageOrderSchema, RefInfoSchema
from src.project.utils.query_helper import (
    dump_recent_records,
    find_model,
    get_all_records,
    get_next_id,
    get_record_by_id,
    get_record_by_name,
    get_record_by_page_clue,
    get_record_by_page_name,
    search_records,
)


class TestQueryHelpers:
    def test_get_next_id(self, app, session):
        next_id = get_next_id(model=People)
        assert next_id == 6

    def test_get_record_by_id(self, app, session):
        result = get_record_by_id(model=PageRefs, id=3)
        assert result.page == 17
        assert result.people_id == 2

    def test_get_record_by_name(self, app, session):
        result = get_record_by_name(model=People, name="Harry")
        assert result.role == "Murderer"

    def test_get_record_by_page_clue(self, app, session):
        result = get_record_by_page_clue(
            model=ReferenceInfo, page=71, clue="Spartan mother"
        )
        assert result.id == 1
        assert result.info == "Come back with your shield or upon it"

    def test_get_all_records(self, app, session):
        results = get_all_records(model=PageOrder)

        assert results.total == 3

    def test_search_records(self, app, session):
        results = search_records(
            model=PageRefs, filters=[(PageRefs.page == 50), (PageRefs.people_id == 4)]
        )

        assert len(results) == 1
        assert results[0].id == 1

    def test_get_record_by_page_name(self, app, session):
        result = get_record_by_page_name(model=PageRefs, name="Jessica", page=17)

        assert result.id == 3

    def test_dump_recent_records(self, app, session):
        results = dump_recent_records(
            model=ReferenceInfo, schema=RefInfoSchema(), limit=2
        )
        page_numbers = [item.get("page") for item in results]
        assert [16, 71] == page_numbers

    def test_find_model(self, app, session):
        result = find_model(key="pageorder")

        assert result.get("model") == PageOrder
        assert result.get("schema") == PageOrderSchema
