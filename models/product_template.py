from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    show_on_mrp_dashboard = fields.Boolean(
        string="Yönetim Dashboard'da Göster",
        default=False,
        help="Eğer işaretlenirse, bu ürün proje özeti dashboard'undaki üretim tablosunda listelenir."
    )