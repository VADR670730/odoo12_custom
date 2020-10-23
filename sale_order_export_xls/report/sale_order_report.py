# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models


class SalesXlsx(models.AbstractModel):
    _name = 'report.sale_excel_report.sale_report_xls.xslx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, wizard_obj):
        sale_order=self.env['sale.order'].browse(data.get('active_ids'))
        product_ids=self.env['product.product']
        for sale in  sale_order:
            for line in sale.order_line:
                product_ids |= line.product_id

        for obj in wizard_obj:
            if not obj.todas_las_categorias:
                product_ids = self.env['product.product'].search([('id', 'in', product_ids.ids), ('categ_id', 'in',obj.categorias.ids)])
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})
            worksheet.set_column(0, 0, 60)
            row = 0
            col = 1
            for sale in sale_order:
                worksheet.write(row, col, sale.name, text)
                col=col+1
            row = 1
            col = 0
            for product in product_ids:
                worksheet.write(row, col, (product.default_code  if product.default_code else "")+" "+product.name, text)
                for sale in sale_order:
                    col=col+1
                    order_line_ids=self.env['sale.order.line'].search([('id','in',sale.order_line.ids),('product_id','=',product.id)])
                    amount_tax = sum(lines.product_uom_qty for lines in order_line_ids)
                    amount_tax=str(int(float(amount_tax)))
                    if amount_tax=='0':
                        amount_tax=''
                    worksheet.write(row, col,amount_tax, text)
                col = 0
                row=row+1
