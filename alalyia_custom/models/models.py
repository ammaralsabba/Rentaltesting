# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import exceptions
from datetime import datetime
from datetime import timedelta
import re

# class StockMove(models.Model):
#     _inherit = 'stock.picking'
#     _description = 'Stock Serial'
#
#     @api.multi
#     def button_validate(self):
#         res = super(StockMove, self).button_validate()
#         vals_in = self.env['ir.sequence'].next_by_code('stock.in')
#         for record in self:
#                 list_line = []
#                 moves = []
#                 data = {
#                         'name': vals_in,
#                         'partner_id': record.partner_id.id,
#                         'scheduled_date': record.scheduled_date,
#                         'origin': 'Return of %s' %(record.name),
#                         'picking_type_id': 1,
#                         'location_id': 9,
#                         'location_dest_id': 12,
#                 }
#
#
#                 for move in record.move_ids_without_package:
#                     for move_line in move.move_line_ids:
#                         lines = (0, 0, {
#                             'product_id': move_line.product_id.id,
#                             'product_uom_qty': move_line.product_uom_qty,
#                             'product_uom_id': move_line.product_uom_id.id,
#                             'location_id': 9,
#                             'location_dest_id': 12,
#                             'lot_id': move_line.lot_id.id
#                         })
#                         moves.append(lines)
#
#                     line = (0, 0, {
#                         'name': move.product_id.id,
#                         'product_id': move.product_id.id,
#                         'product_uom_qty': move.product_uom_qty,
#                         'product_uom': move.product_uom.id,
#                         'location_id': 9,
#                         'location_dest_id': 12,
#                         'move_line_ids': moves,
#                     })
#                     list_line.append(line)
#
#
#
#                 data['move_ids_without_package'] = list_line
#                 record.create(data)
#         print('Running.....')
#         return res


class MoveLine(models.Model):
    _inherit = 'stock.move.line'
    _description = 'LOT Domain'

    x_returnable = fields.Boolean(string="Returnable", related="product_id.x_returnable")

    @api.onchange('qty_done')
    def onchange_partner(self):
        res = {}
        lot = []
        pick = self.env['stock.picking'].search([('name','=', self.reference)])
        name = pick.origin.replace('Return of ', '')
        pick2 = self.env['stock.picking'].search([('name','=', name)])
        for record in pick2:
           if pick.picking_type_id.id == 1:
            for move in record.move_ids_without_package:
                for move_line in move.move_line_ids:
                    if move_line.lot_id.name != False:
                      lot.append(move_line.lot_id.name)
                      print(lot)
            res['domain'] = {'lot_id': [('name', 'in', lot)]}
           # else:
           #     res['domain'] = {'lot_id': [('product_id', '=', 'parent.product_id')]}
        # for serial in self:
        #     if serial.lot_id.name != False:
        #       if serial.lot_id.name not in lot:
        #           serial.lot_id = ''
        #       if serial.lot_id.name not in lot:
        #           message = 'You can assign only %s to this product' % lot
        #           raise exceptions.Warning(message)
        return res


class Sales(models.Model):
    _inherit = 'sale.order'
    _description = 'Return Order'

    x_return_days = fields.Integer(string='N0. of Days')


class Stock(models.Model):
    _inherit = 'stock.picking'
    _description = 'Return No'

    x_return = fields.Integer(related="sale_id.x_return_days")
    x_return_date = fields.Datetime(string='Return Date', compute="date_addition")

    def date_addition(self):
        for record in self:
            if record.date_done != False:
               #d = record.date_done.strftime('%m/%d/%y')
               #date_1 = datetime.strptime(d, "%m/%d/%y").date()
               #record['x_return_date']= date_1 + timedelta(days=record.x_return)
               record['x_return_date'] =  record.date_done + timedelta(days=record.x_return)



class Product(models.Model):
    _inherit = 'product.template'
    _description = 'Returnable Product'

    x_returnable = fields.Boolean(string="Returnable")