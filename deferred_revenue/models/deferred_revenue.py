# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class DeferredRevenue(models.Model):
    _inherit = "contract.contract"
    _description = ""

    # def validate(self):contract.contract
    #     print("in thefun %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    #     super().validate()
    #     for record in self:
    #         contract_info = {'name': record.name, 'partner_id': 1,'recurring_rule_type':'monthly' if record.method_period==1 else 'yearly',
    #                          'recurring_interval':record.method_number,'contract_total_invoice':record.book_value,'contract_total':record.book_value
    #                          ,'contract_total_remaining':record.value_residual}
    #         filed = self.env['contract.contract'].create(contract_info)
    #         print(filed,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    def action_confirm(self):
        super().action_confirm()
        print("om sub /******************************//////////////////////////*************//////////////")
        x = self.env["account.account"].search([], limit=1)
        for record in self:
            contract_info = {'name': record.name,
                             'method_period': '12' if record.recurring_rule_type == 'monthly' else '12',
                             'method_number': record.recurring_interval, 'book_value': record.contract_total_invoice,
                             'book_value': record.contract_total, 'value_residual': record.contract_total_remaining,
                             'journal_id': record.journal_id.id,'state':'open',
                             'account_depreciation_id': record.type_of_contract.income_account.id, 'asset_type': 'sale',
                             'account_depreciation_expense_id': record.contract_line_fixed_ids.product_id.property_account_income_id.id}
            filed = self.env['account.asset'].create(contract_info)
            print(record.contract_line_fixed_ids.product_id.property_account_income_id.id, "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print(record.contract_line_fixed_ids.product_id.property_account_income_id, "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
