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
	    # Get current day of week and hour
        dow_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        current_datetime = datetime.now()
        current_dow = dow_list[current_datetime.weekday()]
        current_hour = str(current_datetime.hour)
        current_min = str(current_datetime.minute)

        # Request AI_Server
        payload = {'day': current_dow, 'hour': current_min}
        try:
            res = requests.get('http://localhost:8000/recommended_system/product', params=payload)
            product_list = res.json()
            print('-------------------------------------')
            print(res.status_code)
            print(payload)
            pprint(product_list)
            print('-------------------------------------')
            if res.status_code == 200:
                list_product_ids = []
                for p in product_list:
                    list_product_ids.append(p['id_product'])
                str_product_ids = ','.join(s for s in list_product_ids)
                print(str_product_ids)
                await websocket.send(str_product_ids)
            else:
                pass
        except requests.exceptions.RequestException as e:
            print(e)       
        await asyncio.sleep(60)

start_server = websockets.serve(update_qty, 'localhost', 7000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
