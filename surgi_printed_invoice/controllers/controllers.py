# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiPrintedInvoice(http.Controller):
#     @http.route('/surgi_printed_invoice/surgi_printed_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_printed_invoice/surgi_printed_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_printed_invoice.listing', {
#             'root': '/surgi_printed_invoice/surgi_printed_invoice',
#             'objects': http.request.env['surgi_printed_invoice.surgi_printed_invoice'].search([]),
#         })

#     @http.route('/surgi_printed_invoice/surgi_printed_invoice/objects/<model("surgi_printed_invoice.surgi_printed_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_printed_invoice.object', {
#             'object': obj
#         })
