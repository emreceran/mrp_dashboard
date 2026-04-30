from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    # Sadece tabloyu tutacak alan
    production_summary_html = fields.Html(
        string="Üretim Tablosu",
        compute="_compute_production_summary"
    )

    # Projenin genel üretim yüzdesini tutacak alan
    production_percent = fields.Integer(
        string="Üretim Yüzdesi",
        compute="_compute_production_summary"
    )

    # Tabloya tıklayınca Üretim Emirlerini açacak ve ürüne göre gruplayacak fonksiyon
    def action_open_project_mos(self):
        self.ensure_one()
        return {
            'name': f"{self.name} - Üretim Emirleri",
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            # Sihirli dokunuş: group_by ile listeyi açılışta ürünlere göre grupluyoruz
            'context': {
                'default_project_id': self.id,
                'group_by': ['product_id']
            },
            'target': 'current',
        }

    def _compute_production_summary(self):
        # Sütunlarda görmek istediğimiz sabit ürün listesi
        # Şarteli (show_on_mrp_dashboard) açık olan ürünleri bul
        active_products = self.env['product.template'].search([('show_on_mrp_dashboard', '=', True)])

        # Sadece isimlerini çekerek eski FIXED_PRODUCTS yapısı gibi bir string listesi oluştur
        FIXED_PRODUCTS = active_products.mapped('name')

        for project in self:
            stats = {prod: {'bekleyen': 0, 'islemde': 0, 'biten': 0, 'total': 0} for prod in FIXED_PRODUCTS}

            total_bekleyen = 0
            total_islemde = 0
            total_biten = 0
            total_all = 0

            mos = self.env['mrp.production'].search([
                ('project_id', '=', project.id),
                ('state', '!=', 'cancel')
            ])

            for mo in mos:
                tmpl_name = mo.product_id.product_tmpl_id.name or ''
                if tmpl_name in stats:
                    qty = mo.product_qty
                    if mo.state in ['draft', 'confirmed']:
                        stats[tmpl_name]['bekleyen'] += qty
                        total_bekleyen += qty
                    elif mo.state == 'progress':
                        stats[tmpl_name]['islemde'] += qty
                        total_islemde += qty
                    elif mo.state in ['to_close', 'done']:
                        stats[tmpl_name]['biten'] += qty
                        total_biten += qty

                    stats[tmpl_name]['total'] += qty
                    total_all += qty

            # Genel Yüzdeyi hesaplayıp yeni alana yazıyoruz
            prod_percent = int((total_biten / total_all) * 100) if total_all > 0 else 0
            project.production_percent = prod_percent

            # Ürün isminin altında Progress Bar olan HTML Tablomuz
            table_html = """
            <table class="table table-sm table-borderless table-hover" style="font-size: 10px; line-height: 1.1; margin-bottom: 0;">
                <thead>
                    <tr style="border-bottom: 1px solid #ccc;">
                        <th style="padding: 2px 0;">Ürün</th>
                        <th class="text-center text-muted" style="padding: 2px 0;">Bekleyen</th>
                        <th class="text-center text-warning" style="padding: 2px 0;">İşlemde</th>
                        <th class="text-center text-success" style="padding: 2px 0;">Biten</th>
                        <th class="text-center text-primary" style="padding: 2px 0;">Top.</th>
                    </tr>
                </thead>
                <tbody>
            """

            for tmpl in FIXED_PRODUCTS:
                data = stats[tmpl]
                p_total = data['total']
                p_done = data['biten']

                # Her bir ürün için alt % hesaplama
                p_percent = int((p_done / p_total) * 100) if p_total > 0 else 0

                # Progress Bar Rengi: %100 ise yeşil, 0 ise gri, arasıysa mavi
                bar_color = "bg-success" if p_percent == 100 else "bg-primary"
                if p_percent == 0:
                    bar_color = "bg-secondary"

                table_html += f"""
                    <tr style="border-bottom: 1px dashed #eee;">
                        <td style="padding: 3px 0; max-width: 100px;">
                            <div class="d-flex justify-content-between align-items-center">
                                <strong class="text-truncate" title="{tmpl}">{tmpl}</strong>
                                <span style="font-size: 8px; font-weight: bold; color: #666;">%{p_percent}</span>
                            </div>
                            <div class="progress" style="height: 3px; width: 100%; margin-top: 2px; background-color: #e9ecef;">
                                <div class="progress-bar {bar_color}" role="progressbar" style="width: {p_percent}%;"></div>
                            </div>
                        </td>
                        <td class="text-center text-muted align-middle" style="padding: 3px 0;">{data['bekleyen']}</td>
                        <td class="text-center text-warning align-middle" style="padding: 3px 0;">{data['islemde']}</td>
                        <td class="text-center text-success align-middle" style="padding: 3px 0;"><strong>{data['biten']}</strong></td>
                        <td class="text-center text-primary align-middle" style="padding: 3px 0;"><strong>{data['total']}</strong></td>
                    </tr>
                """

            table_html += f"""
                </tbody>
                <tfoot>
                    <tr style="border-top: 1px solid #ccc; background-color: #f8f9fa;">
                        <th style="padding: 3px 0;">TOPLAM</th>
                        <th class="text-center text-muted" style="padding: 3px 0;">{total_bekleyen}</th>
                        <th class="text-center text-warning" style="padding: 3px 0;">{total_islemde}</th>
                        <th class="text-center text-success" style="padding: 3px 0;">{total_biten}</th>
                        <th class="text-center text-primary" style="padding: 3px 0;"><strong>{total_all}</strong></th>
                    </tr>
                </tfoot>
            </table>
            """

            project.production_summary_html = table_html