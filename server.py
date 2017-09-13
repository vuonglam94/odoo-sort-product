#!/usr/bin/env python

import asyncio
import websockets
import requests
import functools
import xmlrpc.client
from datetime import datetime
from pprint import pprint

async def update_qty(websocket, path):
    while True:
        flag = ""
        # Configuration
        HOST = 'localhost'
        PORT = 8069
        DB = 'kidzplay_sort'
        USER = 'michael@magestore.com'
        PASS = 'michael123@'
        ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

	    # Get current day of week and hour
        dow_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        current_datetime = datetime.now()
        current_dow = dow_list[current_datetime.weekday()]
        current_hour = str(current_datetime.hour)

	    # Request AI_Server
        payload = {'day': current_dow, 'hour': current_hour}
        try:
            res = requests.get('http://localhost:8000/recommended_system/product', params=payload)
            product_list = res.json()
            print('-------------------------------------')
            print(res.status_code)
            print(payload)
            pprint(product_list)
            print('-------------------------------------')
            if res.status_code == 200:
                # Login
                uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
                print("Logged in as %s (uid:%d)" % (USER, uid))

                call = functools.partial(
                    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
                    DB, uid, PASS)

                # Update records
                for p in product_list:
                    # import pdb
                    # pdb.set_trace()
                    p_id = int(p['id'])
                    p_qty = float(p['qty'])
                    call('product.template', 'write', [p_id], {'qty': p_qty})

                flag = "Done"
            else:
                pass
        except requests.exceptions.RequestException as e:
            print(e)

        await websocket.send(flag)
        print("> {}".format(flag))
        await asyncio.sleep(3600)

start_server = websockets.serve(update_qty, 'localhost', 7000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
