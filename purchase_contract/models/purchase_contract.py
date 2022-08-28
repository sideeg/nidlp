# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class PurchaseContract(models.Model):
    _inherit= "purchase.order"
    _description = ""

    name = fields.Char(string='Account Type', required=True, translate=True)
    contract_no = fields.Char(string="Contract No", help="")
    type = fields.Selection([
        ('PO', 'PO'),
        ('Contract', 'Contract'),],string="Type", required=True, default='Contract',help="")
    contract_type = fields.Selection([
        ('normal', 'Normal'),
        ('critical', 'Critical'),
    ], string="Contract Type",)
    contract_start_date = fields.Date(string="contract start date")
    contract_end_date = fields.Date(string="contract end date")
    remaining_days  = fields.Char(compute="_compute_remaining_days")

    guarantee_visible  = fields.Char(compute="_guarantee_visible",default=0)
    guarantee_value = fields.Char(string="guarantee value")
    guarantee_period = fields.Char(string="guarantee period ")
    bank_name = fields.Char(string="Bank Name", help="")

    @api.depends("contract_start_date","contract_end_date")
    def _compute_remaining_days(self):
        for record in self:
            if record.contract_start_date and record.contract_end_date:
                x=datetime.strptime(str(record.contract_end_date),'%Y-%m-%d') - datetime.strptime(str(record.contract_start_date),'%Y-%m-%d')
                print(x,type(x),str(x) )
                record.remaining_days = record.contract_end_date - record.contract_start_date
            else:
                record.remaining_days = 0

    @api.depends("amount_total")
    def _guarantee_visible(self):
        for record in self:
            if record.amount_total >= 300000:
                record.guarantee_visible  =1
            else:
                record.guarantee_visible = 0

    def _ir_cron_auto_notification(self):
        print(self,type(self),"##########################################################################")
        for record in self:
            print("Inside the function%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            x = datetime.strptime(str(record.contract_end_date), '%Y-%m-%d') - datetime.strptime(str(datetime.now(), '%Y-%m-%d'))
            print(x , str(x).replace("days",""))
            users = self.env['res.users'].search([])
            for user  in users :
                if user.has_group('purchase.group_purchase_manager'):
                    record.activity_scheduale('Applicant Request',user_id=user.id)

    def po_full_billed(self):
        for rec in  self:
            rec.invoice_status = 'invoiced'