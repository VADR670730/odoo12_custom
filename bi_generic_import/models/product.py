# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import tempfile
import binascii
import xlrd
from odoo.exceptions import Warning
from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class gen_product(models.TransientModel):
    _name = "gen.product"

    file = fields.Binary('File')

    @api.multi
    def create_product(self, values):
        product_categ_obj = self.env['product.category']
        product_pricelist = self.env['product.pricelist']
        if values.get('categ_id') == '':
            raise Warning('CATEGORY field can not be empty')
        else:
            categ_id = product_categ_obj.search([('name', '=', values.get('categ_id'))])

        p = self.env['product.template'].search([('default_code', '=', values.get('default_code'))])

        if values.get('type') == 'Consumable':
            type = 'consu'
        elif values.get('type') == 'Service':
            type = 'service'
        elif values.get('type') == 'Stockable Product':
            type = 'product'

        item=self.env['product.pricelist.item']
        if values.get('A').strip():
            pricelist=product_pricelist.search([('name', '=', 'A')])
            r=item.create({
                'pricelist_id': pricelist.id,
                'fixed_price': float(values.get('A'))
                 })
            p.item_ids+=r
        if values.get('B').strip():
            pricelist = product_pricelist.search([('name', '=', 'B')])
            r = item.create({
                'pricelist_id': pricelist.id,
                'fixed_price': float(values.get('B'))
            })
            p.item_ids += r
        if values.get('C').strip():
            pricelist = product_pricelist.search([('name', '=', 'C')])
            r = item.create({
                'pricelist_id': pricelist.id,
                'fixed_price': float(values.get('C'))
            })
            p.item_ids += r
        if values.get('D').strip():
            pricelist = product_pricelist.search([('name', '=', 'D')])
            r = item.create({
                'pricelist_id': pricelist.id,
                'fixed_price': float(values.get('D'))
            })
            p.item_ids += r
        vals = {
           # 'name': values.get('name'),
            #'default_code': values.get('default_code'),
            'categ_id': categ_id.id,
            'type': type,
            'standard_price': values.get('cost_price'),
        }
        res =p.write(vals)
        print(vals)
        return res

    @api.multi
    def import_product(self):

        fp = tempfile.NamedTemporaryFile(suffix=".xlsx",delete=False)
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        for row_no in range(sheet.nrows):
            val = {}
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(
                    map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                        sheet.row(row_no)))
                values.update({
                    'categ_id': line[1],
                    'name': line[2],
                    'default_code': line[3],
                    'cost_price': line[5],
                    'type': "Consumable",
                    'uom': "Unit(s)",
                    'po_uom': "Unit(s)",
                    # 'sale_price': line[7],
                    'A': line[6],
                    'B': line[7],
                    'C': line[8],
                    'D': line[9],
                })
                res = self.create_product(values)

        return res
