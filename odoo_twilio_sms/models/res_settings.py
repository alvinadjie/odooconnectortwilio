from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    twilio_account_sid = fields.Char("Twilio Account SID", related="company_id.twilio_account_sid", readonly=False)
    twilio_auth_token = fields.Char("Twilio Auth Token", related="company_id.twilio_auth_token", readonly=False)
    twilio_number = fields.Char("Twilio Number", related="company_id.twilio_number", readonly=False)
