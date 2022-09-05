# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class AccountAssetWithPurchase(models.Model):
    _inherit= "account.asset"
    _description = ""

    bill_ref  = fields.Char(string='Bill Ref ', compute="_compute_resource_ref",translate=True)
    vendor = fields.Char(string="Vendor ", help="",compute="_compute_resource_ref")

    @api.depends('original_move_line_ids')
    def _compute_resource_ref(self):
        for line in self:
            line.vendor = ''
            line.bill_ref = 0
            if len(line.original_move_line_ids) > 0:
                record =(line.original_move_line_ids[0].partner_id.name) #self.env[line.original_move_line_ids]._search([], limit=1)
                line.vendor = (line.original_move_line_ids[0].partner_id.name)
                line.bill_ref = line.original_move_line_ids[0].ref
            for rec in line.original_move_line_ids:
                print(rec.move_id)
                print(len(rec.move_id) , rec.name)


