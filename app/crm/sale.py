from app.crm.operations.exports import export_orders


def sale_router(args, data):
    mode = args['mode']

    if mode == 'checkauth':
        return 'success\r\ntest\r\ntest'
    elif mode == 'query':
        res = export_orders()
        return res
    return '', 404
