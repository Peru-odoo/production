# -*- coding: utf-8 -*-
# from odoo import http


# class surgi-sales-discount(http.Controller):
#     @http.route('/surgi-sales-discount/surgi-sales-discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi-sales-discount/surgi-sales-discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi-sales-discount.listing', {
#             'root': '/surgi-sales-discount/surgi-sales-discount',
#             'objects': http.request.env['surgi-sales-discount.surgi-sales-discount'].search([]),
#         })

#     @http.route('/surgi-sales-discount/surgi-sales-discount/objects/<model("surgi-sales-discount.surgi-sales-discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi-sales-discount.object', {
#             'object': obj
#         })
