from odoo import fields, models, tools


class Currency(models.Model):
    _inherit = "res.currency"

    symbol = fields.Char(translate=True)


class Countries(models.Model):
    _inherit = "res.country"

    name = fields.Char(translate=True)


class Bank(models.Model):
    _name = "res.bank"
    _inherit = ['res.bank', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(translate=True, track_visibility='onchange')


class PartnerBank(models.Model):
    _name = "res.partner.bank"
    _inherit = ['res.partner.bank', 'mail.thread', 'mail.activity.mixin']

    acc_number = fields.Char('Account Number', required=True, track_visibility='onchange')
    bank_id = fields.Many2one('res.bank', string='Bank', track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', 'Account Holder', ondelete='cascade', index=True,
                                 domain=['|', ('is_company', '=', True), ('parent_id', '=', False)], required=True,
                                 track_visibility='onchange')


class ResUsers(models.Model):
    _inherit = 'res.users'

    sign_signature = fields.Binary(string="Digital Signature", groups="")
    sign_initials = fields.Binary(string="Digitial Initials", groups="")
