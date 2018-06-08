from aiohttp import web
from bson.objectid import ObjectId
from .utils import JSONEncoder

encoder = JSONEncoder()


async def get_root_nodes(request):
    ''' Return array of root tree nodes in JSON format '''
    # get db collection
    collection = request.app['collection']
    # get documents(only id and name) without parent
    cursor = collection.find({'parent': None}, {'_id': 1, 'name': 1})
    response = await cursor.to_list(length=None)
    return web.json_response(body=encoder.encode(response))


async def get_child_nodes(request):
    ''' Return array of child nodes with given parent'''
    collection = request.app['collection']
    parent_id = request.match_info['parentId']
    # documents(only id and name) with given parent
    cursor = collection.find({'parent': ObjectId(parent_id)},
                             {'_id': 1, 'name': 1})
    response = await cursor.to_list(length=None)
    return web.json_response(body=encoder.encode(response))


async def get_node_data(request):
    '''Return object with all node data'''
    collection = request.app['collection']
    id = request.match_info['id']
    # get all data from node with given id
    response = await collection.find_one({'_id': ObjectId(id)})
    return web.json_response(body=encoder.encode(response))
