from odoo import models, fields

class Property(models.Model):
    _name = 'your.module.model'
    _description = 'Description of your model'

    name = fields.Char(string='Name', required=True)