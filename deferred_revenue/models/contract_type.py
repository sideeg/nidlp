from odoo import api, fields, models

class DeferredRevenue(models.Model):
    _inherit = "contract.type"
    _description = ""

    income_account = fields.Many2one(comodel_name='account.account',
                                     # default="sale",
                                     compute="_compute_income_account_id",
                                     inverse="_set_income_account",
                                     # default=lambda self:self.env["account.account"].search([]),
                                     # default=lambda self: self.env['account.account'].search([]),
                                     # required=False,
                                     readonly=False,
                                     # store=True,

                                     )

    # defaults = {
    #     'income_account': _compute_income_account_id,
    # }

    @api.model
    @api.depends('income_account')
    def _compute_income_account_id(self):
        Accounts = self.env["account.account"]
        print(Accounts.search([], limit=1), '//////////////////////////////////////////////////////////////')
        # return Accounts.search([], limit=1)
        for contract in self:
            if not contract.income_account:
                account = Accounts.search([], limit=1)
                print(contract.income_account,
                      '**********************************************************************************')

                if account:
                    contract.income_account = account.id
            else:
                print(
                    "in else +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                contract.income_account = contract.income_account

    def _set_income_account(self):
        pass