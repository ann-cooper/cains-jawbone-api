from tests import params 
import pytest
from src.project.forms import CharacterForm


class TestCharacters:
    @pytest.mark.parametrize("id, endpoint, expected", params.characters_get_params, ids=params.characters_get_ids)
    def test_get_characters(self, app, client, id, endpoint, expected):
        response = client.get(endpoint)
        assert response.status_code == expected

    def test_post_characters(self, app, session, client):
        form = CharacterForm(data={"name": "Test Character", "role": "Unknown", "page": 30})     
        response = client.post("/characters/", data=form.data, follow_redirects=True)
        print(response.status_code, response.json)
        # TODO lookup new record and assert