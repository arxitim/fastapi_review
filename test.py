import pytest
import pytest_mock
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
@pytest_mock.mock.patch('main.users_query_exe', return_value=[["2020-10-27", 1],
                                                              ["2020-10-27", 2],
                                                              ["2020-10-27", 3],
                                                              ["2020-10-27", 1],
                                                              ["2020-10-27", 2],
                                                              ["2020-10-27", 3]])
async def test_users(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users")
    assert response.status_code == 200
    assert response.json() == {'data': {
                                        '0': {'count': 1, 'date': '2020-10-27'},
                                        '1': {'count': 2, 'date': '2020-10-27'},
                                        '2': {'count': 3, 'date': '2020-10-27'},
                                        '3': {'count': 1, 'date': '2020-10-27'},
                                        '4': {'count': 2, 'date': '2020-10-27'},
                                        '5': {'count': 3, 'date': '2020-10-27'}
                                        }
                               }


@pytest.mark.asyncio
@pytest_mock.mock.patch('main.action_query_exe', return_value=[["2020-10-27", 1, "schedule"],
                                                                ["2020-10-27", 2, "schedule"],
                                                                ["2020-10-27", 3, "help"],
                                                                ["2020-10-27", 4, "invalid"],
                                                                ["2020-10-27", 5, "invalid"],
                                                                ["2020-10-27", 6, "schedule"],])
async def test_actions(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/actions")
    assert response.status_code == 200
    assert response.json() == {'data': {'0': {'action': 'schedule', 'count': 1, 'date': '2020-10-27'},
                                        '1': {'action': 'schedule', 'count': 2, 'date': '2020-10-27'},
                                        '2': {'action': 'help', 'count': 3, 'date': '2020-10-27'},
                                        '3': {'action': 'invalid', 'count': 4, 'date': '2020-10-27'},
                                        '4': {'action': 'invalid', 'count': 5, 'date': '2020-10-27'},
                                        '5': {'action': 'schedule', 'count': 6, 'date': '2020-10-27'}}}


@pytest.mark.asyncio
@pytest_mock.mock.patch('main.action_query_exe', return_value=[["2020-10-27", 1, "schedule"],
                                                              ["2020-10-27", 2, "schedule"],
                                                              ["2020-10-27", 3, "help"],
                                                              ["2020-10-27", 4, "invalid"],
                                                              ["2020-10-27", 5, "invalid"],
                                                              ["2020-10-27", 6, "schedule"],])
async def test_usage(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/usage")
    assert response.status_code == 200
    assert response.json() == {'data':
                                    {'0': {'actions':
                                               ['schedule',
                                                'schedule',
                                                'help',
                                                'invalid',
                                                'invalid',
                                                'schedule'],
                                           'count': 0,
                                           'date': '2020-10-27'}}}
