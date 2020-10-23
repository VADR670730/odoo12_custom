# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models, fields, api, _
import time
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class SalesXlsx(models.AbstractModel):
    _name = 'report.reporte_mayoreo.venta_report_excel'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, wizard_obj):
        now=datetime.now()
        for obj in wizard_obj:
            domain=[]
            if obj.fecha_inicio:
                domain.append(('confirmation_date', '>=', obj.fecha_inicio))
            if obj.fecha_inicio:
                domain.append(('confirmation_date', '<=', obj.fecha_fin))
            if obj.comercial:
                domain.append(('user_id', '=', obj.comercial.name))

            sale_order = self.env['sale.order'].search([])
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})
            hoja = 1
            worksheet.set_column(0, 0, 60)
            worksheet.write('A' + str(hoja), 'REPORTE DE VENTAS SUPERMERCADOSDIGITAL-SMD MAYOREO', bold)
            worksheet.write('I' + str(hoja), 'Fecha y hora de generacion del reporte', text)
            worksheet.write('B' + str(hoja + 2), 'Periodo del ' +str(obj.fecha_inicio)+' al '+str(obj.fecha_fin), text)
            worksheet.write('A' + str(hoja + 3), 'Ruta:', text)
            worksheet.write('D' + str(hoja + 4), 'Nombre del vendedor: '+ obj.comercial.name, text)
            worksheet.write('E' + str(hoja + 6), 'AREA DE COBRO', text)
            worksheet.write('A' + str(hoja + 7), 'Monto Cobrado incluyendo impuesto sobre ventas:', text)
            worksheet.write('G' + str(hoja + 7), 'Monto cobrado sin Impuestos sobre ventas:', text)
            worksheet.write('A' + str(hoja + 9), 'Porcentaje de morosidad de cartera', text)
            worksheet.write('E' + str(hoja + 12), 'AREA DE VENTA', text)
            worksheet.write('A' + str(hoja + 13), 'Descripcion ', bold)
            worksheet.set_column(0,14, 20)
            worksheet.write('B' + str(hoja + 13), 'Meta Monto ', bold)
            worksheet.set_column(1,14, 20)
            worksheet.write('C' + str(hoja + 13), 'Venta Monto ', bold)
            worksheet.set_column(2,14, 20)
            worksheet.write('D' + str(hoja + 13), 'Tarifa A', bold)
            worksheet.set_column(3,14,20)
            worksheet.write('E' + str(hoja + 13), 'Tarifa B ', bold)
            worksheet.set_column(4,14, 20)
            worksheet.write('F' + str(hoja + 13), 'Tarifa C ', bold)
            worksheet.set_column(5,14, 20)
            worksheet.write('G' + str(hoja + 13), 'Tarifa D ', bold)
            worksheet.set_column(6,14, 20)
            worksheet.write('H' + str(hoja + 13), 'Comision ', bold)
            worksheet.set_column(7,14, 20)
            row = hoja + 13
            col = 0
            data = {}
            total = 0
            total_con_impuesto=0
            for sale in sale_order:
                for line in sale.order_line:
                    data.setdefault(line.product_id.brand_id.id, {'Descripcion': line.product_id.brand_id.name,"Meta Monto":0,"Venta Monto":0, 'A': 0})
                    data[line.product_id.brand_id.id]['Venta Monto'] += line.price_subtotal
                    total += line.price_unit
                    total_con_impuesto += line.price_subtotal
                    if line.order_id.pricelist_id.name == "A":
                        data[line.product_id.brand_id.id]['A'] += line.price_subtotal
                    if line.order_id.pricelist_id.name == "B":
                        data[line.product_id.brand_id.id]['B'] += line.price_subtotal
                    if line.order_id.pricelist_id.name == "C":
                        data[line.product_id.brand_id.id]['C'] += line.price_subtotal
                    if line.order_id.pricelist_id.name == "D":
                        data[line.product_id.brand_id.id]['D'] += line.price_subtotal

            for key,vals in data.items():
                worksheet.write(row, col, vals['Descripcion'], text)
                worksheet.write(row, col+2, vals['Venta Monto'], text)
                worksheet.write(row, col + 3, vals['A'], text)
                row = row + 1
