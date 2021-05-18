import os
from werkzeug.security import generate_password_hash, check_password_hash

site_login = os.getenv('CRM_LOGIN')
site_password = generate_password_hash(os.getenv('CRM_PASSWORD'))
tmp_catalog = 'crm/tmp/'
max_filesize = 10 * (10 ** 6)

db_login = str(os.getenv('MONGO_USER'))
db_password = str(os.getenv('MONGO_PASS'))
db_name = str(os.getenv('MONGO_DB'))
db_host = str(os.getenv('MONGO_HOST'))
secret_key = str(os.getenv('SECRET_KEY'))
internal_port= os.getenv('INTERNAL_PORT', 5000)

commit_hash = str(os.getenv('COMMIT_HASH', 'development'))
