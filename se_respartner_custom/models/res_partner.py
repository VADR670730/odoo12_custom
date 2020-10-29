# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models,fields
from odoo.exceptions import AccessError


class Partner(models.Model):

    _inherit = ['res.partner']

    ruta = fields.Many2one(comodel_name="partner.ruta", string="Ruta", required=False, )


class PartnerRuta(models.Model):
    _name = 'partner.ruta'

    name = fields.Char()

