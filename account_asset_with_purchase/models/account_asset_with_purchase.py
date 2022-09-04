# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class AccountAssetWithPurchase(models.Model):
    _inherit= "account.asset"
    _description = ""

    bill_ref  = fields.Char(string='Bill Ref ', compute="_compute_resource_ref",translate=True)
    vendor = fields.Char(string="Contract No", help="")

    @api.depends('journal_id')
    def _compute_resource_ref(self):
        print(self,"**************************************************************************************")
        for line in self:
            print(line,"###################################################################################")
            record = self.env[line.journal_id.relation]._search([], limit=1)
            print(record,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4$$$$")


