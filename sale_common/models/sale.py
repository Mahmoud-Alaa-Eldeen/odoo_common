# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    John W. Viloria Amaris <john.viloria.amaris@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api, fields, models
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import pytz

def str_to_datetime(strdate):
    try:
        return datetime.strptime(strdate, DTF)
    except:
        return False

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _utc_to_lctime(self, strdate):
        if self._context is None:
            self._context = {}
        user_tz = pytz.timezone(self._context['tz']) if 'tz' in self._context \
                                else pytz.timezone('America/Bogota')
        date = str_to_datetime(strdate)
        if date:
            today = datetime.today()
            tzoffset = user_tz.utcoffset(today)
            date = date + tzoffset
            return date
        else:
            return False

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        date_order = self._utc_to_lctime(order.date_order)
        if date_order:
            order.date_order_hour = '%s horas' % date_order.strftime('%H')
        return order

    @api.model
    def order_hour_update_all(self):
        orders = self.env['sale.order'].search([])
        for order in orders:
            date_order = self._utc_to_lctime(order.date_order)
            if date_order:
                order.date_order_hour = '%s horas' % date_order.strftime('%H')

    date_order_hour = fields.Char('Sale Hour')