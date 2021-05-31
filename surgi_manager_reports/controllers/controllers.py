# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiManager(http.Controller):
#     @http.route('/surgi_manager_reports/surgi_manager_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_manager_reports/surgi_manager_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_manager_reports.listing', {
#             'root': '/surgi_manager_reports/surgi_manager_reports',
#             'objects': http.request.env['surgi_manager_reports.surgi_manager_reports'].search([]),
#         })

#     @http.route('/surgi_manager_reports/surgi_manager_reports/objects/<model("surgi_manager_reports.surgi_manager_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_manager_reports.object', {
#             'object': obj
#         })
