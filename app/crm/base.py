from app.crm import catalog
import http


def router(args, data):
    op = args['type']

    if op == 'catalog':
        return catalog.catalog_router(args, data)
    return '', 404


