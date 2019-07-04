# -*- coding: utf-8 -*-

"""
Author : Saleh Mahdr

"""
import uuid
from odoo import models, fields, api, _
from datetime import date


class sale_order_line_custom(models.Model):

    #Sale Order line customisation. Create items using odoo inheritence
    _inherit = 'sale.order.line'

    def _get_line(self):
        line_num = 1
        if self.ids:
            first_line = self.browse(self.ids[0])

        for line_rec in first_line.order_id.order_line:
            line_rec.serial_no = line_num
            line_num += 1

    serial_no = fields.Integer(compute='_get_line', string='Serial Number', readonly=False, default=False)


class sale_order_custom(models.Model):
   
    #Sale Order customisation. Create items using odoo inheritence
    _inherit = 'sale.order'

    
    phone_no = fields.Char("Phone")

    @api.multi
    @api.onchange('partner_id')
    def customer_phone(self):
        vals = {}
        vals['phone_no'] = self.partner_id.phone
        self.update(vals)

