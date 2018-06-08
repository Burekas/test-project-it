import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_coro
from bson.objectid import ObjectId
from backend.app import views


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/get-root-nodes', views.get_root_nodes)
    app.router.add_get('/get-child-nodes/{parentId}', views.get_child_nodes)
    app.router.add_get('/get-node-data/{id}', views.get_node_data)
    return loop.run_until_complete(aiohttp_client(app))


async def test_get_root_nodes(cli, mocker):
    id = ObjectId()
    expected_response = [{'Test': 'Test'}, {'_id': id, 'test': 'Test'}]
    cursor = mocker.Mock(to_list=make_mocked_coro(expected_response))
    cli.server.app['collection'] = mocker.Mock()
    find = cli.server.app['collection'].find
    find.return_value = cursor
    resp = await cli.get('/get-root-nodes')
    assert resp.status == 200
    assert await resp.text() == views.encoder.encode(expected_response)
    find.assert_called_once_with(
        {'parent': None}, {'_id': 1, 'name': 1})


async def test_get_child_nodes(cli, mocker):
    parent_id = ObjectId()
    id = ObjectId()
    expected_response = [{'Test': 'Test'}, {'_id': id, 'test': 'Test'}]
    cursor = mocker.Mock(to_list=make_mocked_coro(expected_response))
    cli.server.app['collection'] = mocker.Mock()
    find = cli.server.app['collection'].find
    find.return_value = cursor
    resp = await cli.get(f'/get-child-nodes/{str(parent_id)}')
    assert resp.status == 200
    assert await resp.text() == views.encoder.encode(expected_response)
    find.assert_called_once_with(
        {'parent': parent_id}, {'_id': 1, 'name': 1})


async def test_get_node_data(cli, mocker):
    id = ObjectId()
    expected_response = {'_id': id, 'description': 'TEST'}
    cli.server.app['collection'] = mocker.Mock(find_one=make_mocked_coro(expected_response))
    find_one = cli.server.app['collection'].find_one
    resp = await cli.get(f'/get-node-data/{str(id)}')
    assert resp.status == 200
    assert await resp.text() == views.encoder.encode(expected_response)
    find_one.assert_called_with({'_id': id})
