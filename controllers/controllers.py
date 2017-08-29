# -*- coding: utf-8 -*-
from odoo import http

# class SortProduct(http.Controller):
#     @http.route('/sort_product/sort_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sort_product/sort_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sort_product.listing', {
#             'root': '/sort_product/sort_product',
#             'objects': http.request.env['sort_product.sort_product'].search([]),
#         })

#     @http.route('/sort_product/sort_product/objects/<model("sort_product.sort_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sort_product.object', {
#             'object': obj
#         })