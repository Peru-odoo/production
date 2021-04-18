# -*- coding: utf-8 -*-
# from odoo import http


# class Surgi-total-sale(http.Controller):
#     @http.route('/surgi-total-sale/surgi-total-sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi-total-sale/surgi-total-sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi-total-sale.listing', {
#             'root': '/surgi-total-sale/surgi-total-sale',
#             'objects': http.request.env['surgi-total-sale.surgi-total-sale'].search([]),
#         })

#     @http.route('/surgi-total-sale/surgi-total-sale/objects/<model("surgi-total-sale.surgi-total-sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi-total-sale.object', {
#             'object': obj
#         })
