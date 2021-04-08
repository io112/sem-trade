from flask import Response

from app.crm.operations.exports import export_orders


def sale_router(args, data):
    mode = args['mode']

    if mode == 'checkauth':
        return 'success\r\ntest\r\ntest'
    elif mode == 'query':
        res = Response(export_orders(), mimetype='text/xml')
        return res
    elif mode == 'success':
        return 'success'
    return '', 404
