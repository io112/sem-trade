from app.crm import catalog, sale
import http


def router(args, data):
    op = args['type']

    if op == 'catalog':
        return catalog.catalog_router(args, data)
    elif op == 'sale':
        return sale.sale_router(args, data)
    return '', 404


