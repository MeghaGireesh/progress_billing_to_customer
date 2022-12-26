from odoo import models, fields, api


class InvoiceInherit(models.Model):
    _inherit = 'account.move'

    progress_bill_title = fields.Char(string='Progress Billing Title')
    project_id = fields.Many2one('account.analytic.account', string='Project', copy=False)
    total_progress_billing = fields.Float(string="Total Progress Billing",
                                          compute='_compute_total_progress_bill',
                                          copy=False, store=True)
    invoice_to_date = fields.Float(string="Invoice To Date",
                                   compute='_compute_invoice_to_date', copy=False,
                                   store=True)
    remaining_progress_billing = fields.Float(string="Remaining Progress Billing",
                                              compute='_compute_remaining_progress_billing',
                                              copy=False, store=True)
    previously_invoice = fields.Float(string="Previously Invoiced",
                                      compute='_compute_previously_invoiced', copy=False,
                                      store=True)
    previously_invoice_due = fields.Float(string="Previously Invoiced Due",
                                          compute='_compute_previously_invoiced',
                                          copy=False, store=True)
    current_invoice = fields.Float(string="Current Invoiced",
                                   compute='_compute_current_invoiced', copy=False,
                                   store=True)
    less_paid_amount = fields.Float(string="Less Paid Amount",
                                    compute='_compute_less_paid_amount', copy=False,
                                    store=True)
    total_due = fields.Float(string="Total Due", compute='_compute_total_due',
                             copy=False, store=True)

    @api.depends('project_id')
    def _compute_total_progress_bill(self):
        for rec in self:
            rec.total_progress_billing = rec.project_id.total_progress_billing

    @api.depends('project_id', 'amount_total')
    def _compute_invoice_to_date(self):
        for rec in self:
            rec.invoice_to_date = 0
            if rec.project_id:
                invoice = self.search(
                    ['|', ('state', 'in', ['posted']), ('payment_state', 'in', ['paid']),
                     ('move_type', '=', 'out_invoice'),
                     ('partner_id', '=', rec.partner_id.id),
                     ('project_id', '=', rec.project_id.id)])
                print('sss', invoice)
                for val in invoice:
                    rec.invoice_to_date = rec.invoice_to_date + val.amount_total

    @api.depends('total_progress_billing', 'invoice_to_date')
    def _compute_remaining_progress_billing(self):
        for rec in self:
            rec.remaining_progress_billing = rec.total_progress_billing - rec.invoice_to_date

    @api.depends('project_id', 'amount_total', 'amount_residual')
    def _compute_previously_invoiced(self):
        for rec in self:
            rec.previously_invoice = 0
            rec.previously_invoice_due = 0
            if rec.project_id:
                invoice = self.search(['|', ('state', 'in', ['posted']),
                                       ('payment_state', 'in', ['paid']),
                                       ('move_type', '=', 'out_invoice'),
                                       ('partner_id', '=', rec.partner_id.id),
                                       ('project_id', '=', rec.project_id.id)])
                if len(invoice) == 1:
                    rec.previously_invoice = 0
                if len(invoice) > 1:
                    rec.previously_invoice = 0
                    for val in invoice:
                        if val.id != rec.id:
                            rec.previously_invoice += val.amount_total
                            rec.previously_invoice_due += val.amount_residual

    @api.depends('amount_total')
    def _compute_current_invoiced(self):
        for rec in self:
            rec.current_invoice = rec.amount_total

    @api.depends('amount_residual')
    def _compute_less_paid_amount(self):
        for rec in self:
            rec.less_paid_amount = rec.amount_residual

    @api.depends('less_paid_amount', 'previously_invoice', 'current_invoice')
    def _compute_total_due(self):
        for rec in self:
            rec.total_due = rec.previously_invoice_due + rec.less_paid_amount
