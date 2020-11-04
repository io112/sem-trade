from app.constants import max_filesize, tmp_catalog
from app.crm.operations import imports
from os import path
import zipfile
import io
from lxml import etree


def catalog_router(args, data):
    mode = args['mode']

    if mode == 'checkauth':
        return 'success\r\ntest\r\ntest'
    if mode == 'init':
        return f'zip=yes\r\nfile_limit={max_filesize}'
    if mode == 'file':
        z = zipfile.ZipFile(io.BytesIO(data))
        z.extractall(tmp_catalog)
        z.close()
        return 'success'
    if mode == 'import':
        try:
            tree = etree.parse(path.join(tmp_catalog, args['filename']))
        except:
            return 'fail'
        imports.import_data(tree)
        return 'success'
    return '', 404
