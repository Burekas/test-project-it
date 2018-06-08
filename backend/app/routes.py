from .views import get_root_nodes, get_child_nodes, get_node_data


def setup_routes(app):
    app.router.add_get('/api/v1/get-root-nodes', get_root_nodes)
    app.router.add_get('/api/v1/get-child-nodes/{parentId}', get_child_nodes)
    app.router.add_get('/api/v1/get-node-data/{id}', get_node_data)
