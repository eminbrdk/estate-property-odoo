from odoo import models, fields, api, _


class Property(models.Model):
    _name = 'estate.property' #securityde ki estate_property bu, model aramada bunu yaz
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Estate Properties'

    # bir mülkün bir türü olur (apartman, villa), bir tür bir sürü mülkte olabilir (5-6 apartman olabilir mülklerin arasında)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    # bir mülkün bir sürü etiketi (bir ev hem rahat, hem güneşli olabilir), bir etiket bir sürü mülkte bulunabilir (rahat bir sürü ev olabilir)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    # bir mülke bir sürü talep gelebilir, bir talep bir mülke aittir
    # one to many oldumu diğer tarafta many to one yapmalaısın
    property_offer_ids = fields.One2many("estate.property.offer", "property_id" , string="Property Offers")
    #sistemdeki biri olabilir, res kullan. yada users ve partner odoo da var ondan oluşturmayıp res yaptık
    sales_id = fields.Many2one("res.users", string="Salesman")
    # domain ile partnerlerin is_company = true olanları aldık yani filtreledik
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain=[("is_company", "=", True)])

    name = fields.Char(string='Name', required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("accepted", " Offer Accepted"),
            ("received", " Offer Received"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        string="Status",
        default="new"
    )
    description = fields.Char(string="Description")
    postcode = fields.Char(string="Postcode", tracking=True)
    date_availability = fields.Date(string="Availability Form")
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")
    selling_price = fields.Float(string="Selling Price", compute="_compute_selling_price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
        default="north"
    )
    # related ile buyer seçildiğinde phone da gösterilecek
    phone = fields.Char(string="Phone", related="buyer_id.phone")

    @api.onchange("living_area", "garden_area")
    def _onchange_total_area(self): #bu fonksiyonun çağırlmadan önce belirtilmesi lazım yani yukarda
        self.total_area = self.living_area + self.garden_area

    total_area = fields.Integer(string="Total Area")

    def sold_pressed(self):
        self.state = "sold"

    def cancel_pressed(self):
        self.state = "cancelled"

    @api.depends("property_offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.property_offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    # object ile yapsaydık böyle yapacaktık ama action ile yaptık o yüzden yoruma aldım
    # xml dosyasında name="action_property_view_offer" type="object" olacaktı
    # def action_property_view_offer(self):
    #    return {
    #        "type": "ir.actions.act_window",
    #        "name": f"{self.name} - Offers",
    #        "domain": [("property_id", "=", self.id)],
    #        "view_model": "tree",
    #        "res_model": "estate.property.offer"
    #    }

    @api.depends("property_offer_ids")
    def _compute_best_offer(self):
        for rec in self:
            if rec.property_offer_ids:
                rec.best_offer = max(rec.property_offer_ids.mapped("price")) #!!!!!!!!!! çokomelli
            else:
                rec.best_offer = 0

    @api.depends("property_offer_ids")
    def _compute_selling_price(self):
        for rec in self:
            rec.selling_price = 0

            if rec.property_offer_ids:
                for a in rec.property_offer_ids.search([("status", "=", "accepted")]):
                    if a["property_id"]["id"] == rec.id:
                        rec.selling_price = a["price"]
                        rec.state = "accepted"

    # reload yazarsan sayfayı yeniler
    # apps yazarsan odoonun ana sayfasına gidersin
    # display_notifification "params": {"title": _("testing client"), "type": "success", "sticky": False} yukardan bildirim çıkartıyor
    def action_client_action(self):
        return {
            "type": "ir.actions.client",
            "tag": "reload" # sayfayı yeniledik
        }

    #url action
    def action_url_action(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://www.instagram.com/eminbrdk/",
            "target": "self"
        }

    #report action
    def _get_report_base_filename(self):
        self.ensure_one() # ???
        return "Estate Property - %s" % self.name

    def action_send_email(self):
        mail_template = self.env.ref("deneme_ads.offer_mail_template") # recordun id si bu, ona eriştik
        mail_template.send_mail(self.id, force_send=True)

    def _get_emails(self): # bununla gönderilecek mailleri aldık ve virgül ile listeledik. Çünkü, istenilen format bu
        emails = ",".join(self.property_offer_ids.mapped("partner_email"))
        print(emails)
        return emails

    def _get_sender_email(self):
        e = self.env.user["email"]
        print(e)
        return e

    def _get_buyer_name(self):
        name = "kimse"
        print("a")
        for offer in self.property_offer_ids:
            if offer["status"] == "accepted":
                name = offer["partner_id"]["name"]
        print(name)
        return name


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Estate Property Types'

    name = fields.Char(string='Name', required=True)


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = 'Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string="Color")