# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiWarehouseUsers(http.Controller):
#     @http.route('/surgi_warehouse_users/surgi_warehouse_users/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_warehouse_users/surgi_warehouse_users/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_warehouse_users.listing', {
#             'root': '/surgi_warehouse_users/surgi_warehouse_users',
#             'objects': http.request.env['surgi_warehouse_users.surgi_warehouse_users'].search([]),
#         })

#     @http.route('/surgi_warehouse_users/surgi_warehouse_users/objects/<model("surgi_warehouse_users.surgi_warehouse_users"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_warehouse_users.object', {
#             'object': obj
#         })
