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
        for obj in wizard_obj:
            domain=[]
            periodo=False
            if obj.fecha_inicio:
                domain.append(('confirmation_date', '>=', obj.fecha_inicio))
                periodo=str(obj.fecha_inicio)
            if obj.fecha_inicio:
                domain.append(('confirmation_date', '<=', obj.fecha_fin))
                periodo+=+' al '+str(obj.fecha_fin)
            if obj.comercial:
                domain.append(('user_id', '=', obj.comercial.name))

            domain.append(('state', 'not in', ['draft','cancel']))

            sale_order = self.env['sale.order'].search(domain)
            print(sale_order)
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})
            hoja = 1
            worksheet.set_column(0, 0, 60)
            worksheet.write('A' + str(hoja), 'REPORTE DE VENTAS SUPERMERCADOSDIGITAL-SMD MAYOREO', bold)
            worksheet.write('I' + str(hoja), 'Fecha y hora de generacion del reporte: '+str(fields.Datetime.now()), text)
            if periodo:
                worksheet.write('B' + str(hoja + 2), 'Periodo del ' +periodo, text)

            if obj.comercial:
                worksheet.write('A' + str(hoja + 3), 'Ruta: ' + obj.comercial.name, text)
            worksheet.write('E' + str(hoja + 6), 'AREA DE COBRO', text)

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
            total = sum([s.amount_untaxed for s in sale_order])
            total_con_impuesto=sum([s.amount_total for s in sale_order])
            worksheet.write('A' + str(hoja + 7), 'Monto Cobrado incluyendo impuesto sobre ventas: '+str(total_con_impuesto), text)
            worksheet.write('G' + str(hoja + 7), 'Monto cobrado sin Impuestos sobre ventas: '+str(total), text)

            for sale in sale_order:
                for line in sale.order_line:
                    data.setdefault(line.product_id.brand_id.id, {'Descripcion': line.product_id.brand_id.name,"Meta Monto":0,"Venta Monto":0, 'A': 0, 'B': 0, 'C': 0, 'D': 0,'Comision': 0})
                    data[line.product_id.brand_id.id]['Venta Monto'] += line.price_subtotal
                    total += line.price_unit
                    total_con_impuesto += line.price_subtotal
                    data[line.product_id.brand_id.id]['Comision'] += (line.price_subtotal*line.price_list_id.porciento_ganancia)/100
                    if line.price_list_id.name == "A":
                        data[line.product_id.brand_id.id]['A'] += line.price_subtotal
                    if line.price_list_id.name == "B":
                        data[line.product_id.brand_id.id]['B'] += line.price_subtotal
                    if line.price_list_id.name == "C":
                        data[line.product_id.brand_id.id]['C'] += line.price_subtotal
                    if line.price_list_id.name == "D":
                        data[line.product_id.brand_id.id]['D'] += line.price_subtotal

            for key,vals in data.items():
                worksheet.write(row, col, vals['Descripcion'], text)
                worksheet.write(row, col+2, vals['Venta Monto'], text)
                worksheet.write(row, col + 3, vals['A'], text)
                worksheet.write(row, col + 4, vals['B'], text)
                worksheet.write(row, col + 5, vals['C'], text)
                worksheet.write(row, col + 6, vals['D'], text)
                worksheet.write(row, col + 7, vals['Comision'], text)
                row = row + 1
