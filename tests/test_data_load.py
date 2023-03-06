from src import logger
from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.utils.query_helper import get_all_records

logger = logger.get_logger(__name__)


class TestDataLoad:
    def test_load_pg_data(self, app, session):
        check_people = get_all_records(model=People)
        check_page_refs = get_all_records(model=PageRefs)
        check_page_order = get_all_records(model=PageOrder)
        check_ref_info = get_all_records(model=ReferenceInfo)

        assert check_people.total == 4
        assert check_page_refs.total == 3
        assert check_page_order.total == 3
        assert check_ref_info.total == 3
