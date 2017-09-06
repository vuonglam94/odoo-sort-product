# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import functools
import xmlrpclib
from datetime import datetime
from pytz import timezone
from pprint import pprint

class Product(models.Model):
    _inherit = 'product.template'

    qty = fields.Float(string='qty', default=0.0)

    def _cron_update_qty(self):
        # Configuration
        HOST = 'localhost'
        PORT = 8069
        DB = 'kidzplay_sort'
        USER = 'michael@magestore.com'
        PASS = 'michael123@'
        ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)
        TIMEZONE = 'Asia/Ho_Chi_Minh'

        # Get current day of week and hour
        dow_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        current_datetime = datetime.now(timezone('UTC')).astimezone(timezone(TIMEZONE))
        current_dow = dow_list[current_datetime.weekday()]
        current_hour = str(current_datetime.hour)

        # Request AI_Server
        payload = {'day': current_dow, 'hour': current_hour}
        try:
            res = requests.get('http://localhost:8000/recommended_system/product', params=payload)
            product_list = res.json()
            print '-------------------------------------'
            print res.status_code
            print payload
            pprint(product_list)
            print '-------------------------------------'
            if res.status_code == 200:
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
            else:
                pass
        except requests.exceptions.RequestException as e:
            print e
