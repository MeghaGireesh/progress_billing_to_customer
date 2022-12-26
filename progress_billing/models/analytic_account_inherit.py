from odoo import models, fields, api


class AnalyticAccountInherit(models.Model):
    _inherit = 'account.analytic.account'

    total_progress_billing = fields.Float(copy=False)
