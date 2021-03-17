import os
from werkzeug.security import generate_password_hash, check_password_hash

site_login = os.getenv('1C_LOGIN')
site_password = generate_password_hash(os.getenv('1C_PASSWORD'))
tmp_catalog = 'crm/tmp/'
max_filesize = 10 * (10 ** 6)

db_login = str(os.getenv('MONGO_USER'))
db_password = str(os.getenv('MONGO_PASS'))
db_name = str(os.getenv('MONGO_DB'))
db_host = str(os.getenv('MONGO_HOST'))
secret_key = str(os.getenv('SECRET_KEY'))
