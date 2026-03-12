from odoo import models, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def action_open_mo(self):
        self.ensure_one()
        return {
            'name': 'Üretim Emri',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'res_id': self.production_id.id,
            'view_mode': 'form',
            'target': 'current',
        }