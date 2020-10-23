# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PriceList(models.Model):

    _inherit = 'product.pricelist'

    porciento_ganancia = fields.Float(string="% de Ganancia",  required=False,default=1 )