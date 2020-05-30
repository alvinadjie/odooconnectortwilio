
from odoo import models, fields, _
from odoo.exceptions import ValidationError, Warning
default_content_confirm = 'Hi ${object.partner_id.name} Your order has been proceed'

class ResCompany(models.Model):
    _inherit = "res.company"

    twilio_account_sid = fields.Char()
    twilio_auth_token = fields.Char()
    twilio_number = fields.Char()
    sms_content_confirm = fields.Text(default=default_content_confirm)
