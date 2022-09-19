# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    contract_id = fields.Many2one(
        'contract.contract',
        readonly=True,
        copy=True
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    contract_line_id = fields.Many2one(
        'contract.line',
        readonly=True,
        copy=True
    )
