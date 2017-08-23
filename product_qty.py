import json
from pprint import pprint
import requests
import functools
import xmlrpclib

# Call api
payload = {'day': 'sunday', 'hour': '9'}
res = requests.get('http://localhost:8000/recommended_system/product', params=payload)
product_list = res.json()

# Configuration
HOST = 'localhost'
PORT = 8069
DB = 'kidzplay_test'
USER = 'michael@magestore.com'
PASS = 'michael123@'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print "Logged in as %s (uid:%d)" % (USER,uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)
# Update records
for p in product_list:
	# import pdb
	# pdb.set_trace()
	p_id = int(p['id'])
	p_qty = float(p['qty'])
	p_updated = call('product.template', 'write', [p_id], {'qty': p_qty})