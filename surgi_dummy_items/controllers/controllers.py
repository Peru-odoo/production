# -*- coding: utf-8 -*-
# from odoo import http


# class Faked-items(http.Controller):
#     @http.route('/surgi_dummy_items/surgi_dummy_items/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_dummy_items/surgi_dummy_items/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_dummy_items.listing', {
#             'root': '/surgi_dummy_items/surgi_dummy_items',
#             'objects': http.request.env['surgi_dummy_items.surgi_dummy_items'].search([]),
#         })

#     @http.route('/surgi_dummy_items/surgi_dummy_items/objects/<model("surgi_dummy_items.surgi_dummy_items"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_dummy_items.object', {
#             'object': obj
#         })
