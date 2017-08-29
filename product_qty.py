import requests
import functools
import xmlrpclib
from datetime import datetime
from pprint import pprint

# Get current day of week and hour
dow_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
current_dow = dow_list[datetime.today().weekday()]
current_hour = str(datetime.now().hour)

# Call api
payload = {'day': current_dow, 'hour': current_hour}
res = requests.get('http://localhost:8000/recommended_system/product', params=payload)
product_list = res.json()
print('-------------------------------------')
print(datetime.now())
print(payload)
pprint(product_list)
print('-------------------------------------')

# Configuration
HOST = 'localhost'
PORT = 8069
DB = 'kidzplay_sort'
USER = 'michael@magestore.com'
PASS = 'michael123@'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print "Logged in as %s (uid:%d)" % (USER, uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# Update records
for p in product_list:
    # import pdb
    # pdb.set_trace()
    p_id = int(p['id'])
    p_qty = float(p['qty'])
    call('product.template', 'write', [p_id], {'qty': p_qty})
