# -*- coding: utf-8 -*-
# from odoo import http


# class MrpDashboard(http.Controller):
#     @http.route('/mrp_dashboard/mrp_dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_dashboard/mrp_dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_dashboard.listing', {
#             'root': '/mrp_dashboard/mrp_dashboard',
#             'objects': http.request.env['mrp_dashboard.mrp_dashboard'].search([]),
#         })

#     @http.route('/mrp_dashboard/mrp_dashboard/objects/<model("mrp_dashboard.mrp_dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_dashboard.object', {
#             'object': obj
#         })

