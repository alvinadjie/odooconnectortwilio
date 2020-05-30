# See LICENSE file for full copyright and licensing details.

import pytz
import collections
from pytz import timezone

from odoo import _, api, fields, models
from odoo.tools import ustr, misc, DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.exceptions import ValidationError, Warning
from datetime import timedelta, datetime, time
from odoo.http import request
from twilio.rest import Client


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_reminder = fields.Boolean()
    is_has_phone = fields.Boolean(compute='check_phone_number')
    booking_date_tz = fields.Char()

    @api.onchange('partner_id')
    def check_phone_number(self):
        if self.partner_id.phone:
            self.is_has_phone = True
        else:
            self.is_has_phone = False
    
    def content(self, condition):
        if condition == 'confirm':
            return self.render_sms_confirm(self.id)

    def render_sms_confirm(self, sale_id):
        template = self.env['mail.template']._render_template(self.env.user.company_id.sms_content_confirm, 'sale.order', [sale_id])
        return template[sale_id]
    
    def send_sms(self, condition):
        tz = pytz.timezone(self.env.user.tz) if self.env.user.tz else pytz.utc
        company = self.env.user.company_id
        booking = pytz.utc.localize(self.booking_dt).astimezone(tz)     # convert start in user's timezone
        booking_date = booking.strftime("%Y-%m-%d %H:%M:%S")
        company = self.env.user.company_id
        client = Client(company.twilio_account_sid, company.twilio_auth_token)
        message = client.messages.create(body=self.content(condition), from_=self.env.user.company_id.twilio_number, to=self.partner_id.phone)

        if not message.error_code:
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise Warning("Error Send SMS " + message.error_message)
            

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        condition = 'confirm'
        if self.partner_id.phone:
            self.send_sms(condition)
        elif not self.partner_id.phone:
            raise Warning(_("You Need to set the customer phone number!!"))

