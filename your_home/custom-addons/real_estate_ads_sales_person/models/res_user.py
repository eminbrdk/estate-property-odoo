from odoo import models, api, fields

class Users(models.Model):
    # name yazmadık çünkü sadece 1 tane inherit yapıyoruz
    # bu bir veri tablosu değil sadece res.user'a ekleme yaptık, securitye falan gerek yok bunun için
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "sales_id", string="Properties")