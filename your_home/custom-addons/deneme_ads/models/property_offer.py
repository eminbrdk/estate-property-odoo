from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer' #securityde ki estate_property bu, model aramada bunu yaz
    _description = 'Estate Property Offers'

    # ????? default ayarlarken kullandık
    #@api.model
    #def _set_create_data(self):
    #    return fields.Date.today()

    @api.depends("partner_id", "property_id")
    def _create_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.partner_id.name} - {rec.property_id.name}"
            else:
                rec.name = False

    partner_id = fields.Many2one("res.partner", string="Customer")  # partner oluşturacak mıyız???
    partner_email = fields.Char(string="Customer Email", related="partner_id.email")
    property_id = fields.Many2one("estate.property", string="Property")

    name = fields.Char(string="Description", compute="")
    price = fields.Monetary(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status"
    )
    validity = fields.Integer(string="Validity")
    # compute ile değişiklik olduğunda hesaplıyorsun
    # inverse ile deadline değiştiğinde değişiklik yapıyor ama kaydedince gösteriyor
    deadline = fields.Date(string="Deadline")#, compute="_compute_deadline", inverse="_inverse_deadline")
    creation_date = fields.Date(string="Creation Date")#, default=_set_create_data)
    currency_id = fields.Many2one("res.currency", string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)


    #@api.depends("creation_date", "validity") # bu ikisinden birinde değişiklik oldumu hesaplamayı yapıyor ve gösteriyor
    #def _compute_deadline(self):
    #    for rec in self:
    #        if rec.creation_date and rec.validity:
    #            rec.deadline = rec.creation_date + timedelta(days=rec.validity)
    #        else:
    #            rec.deadline = False
    #
    #def _inverse_deadline(self):
    #    for rec in self:
    #        if rec.deadline and rec.creation_date:
    #            rec.validity = (rec.deadline - rec.creation_date).days
    #        else:
    #            rec.validity = False

    # status = refused olursa unlink ile offer'ı siler. autovacuum sayesinde her gün bakıyor buna
    #@api.autovacuum
    #def _clean_offers(self):
    #    self.search([("status", "=", "refused")]).unlink()

    # ??????
    #@api.model_create_multi
    #def create(self, vals):
    #    for rec in vals:
    #        if not rec.get("creation_date"):
    #            rec["creation_date"] = fields.Date.today()
    #    return super(PropertyOffer, self).create(vals)

    # verileri saveliyeceğimiz zaman uymuyorsa bazı şeyler hata veriyoruz
    #@api.constrains("validity")
    #def _check_validity(self):
    #    for rec in self:
    #        if rec.deadline <= rec.creation_date:
    #            raise ValidationError("Deadline can not be before creation date")
    #
    ##yukardakini yerine şöylede yapabilirsin
    #_sql_constraints = [
    #    ("check_validity", "check(validity > 0)", "Deadline can not be before creation date")
    #]
    #
    ## save dedikten sonra propertyofferda yapılan writeları vals gösteriyor, save dedikten sonra gerçekleşiyor
    #def create(self, vals):
    #    print(vals)
    #
    #    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #    #!!!!!! self.env ile başka modellerede erişim sağlayabiliyorsun. bu çokomelli !!!!!!!!!!!
    #    print(self.env.cr) # current database
    #    print(self.env.uid) # current user id !!!!!!!!! burası önemli
    #    print(self.env.context) # ?????
    #
    #    a = self.env["res.partner"].browse(1) # [1, 3] şeklindede olur
    #    print(a)
    #    print(a["name"])

        # search içine order="name asc/desc" ekleyerek isme göre sıralayabilirsin
        # limit ekleyerek ilk 5i 10u alabilirsin
        # sonuna .unlink() ekleyerek hepsini silebilirsin
        # .mapped('phone') ile for loop kullanmadan hepsinin telefon listesini alırsın
        # .filtered(labda x: x.phone == "1234") ile filtreleme yapabilirsin
    #    b = self.env["res.partner"].search([("is_company", "=", True)])
    #    print(b)
    #    for c in b:
    #        print("--", c["name"], "--")
    #        print("is this a company: ", c["is_company"])
    #
    #    #d = self.env["estate.property.offer"].search([("partner_id", "=", vals[0]["partner_id"])])
    #    #print(d["price"])
    #
    #    return super(PropertyOffer, self).write(vals)

    def action_accept_offer(self):
        self._validate_accepted_offer() # accept etmeden öne başka accept edilen var mı diye baktık !!!
        self.status = "accepted"
        self.property_id.write({
            "state": "accepted"
        })

    def action_refuse_offer(self):
        self.status = "refused"
        if all(self.property_id.property_offer_ids.mapped("status")):
            self.property_id.write({
                "selling_price": 0,
                "state": "received"
            })

    def _validate_accepted_offer(self):
        # önce proprty_id ler uyuşuyor mu ona bakıyoruz, uyuşanların arasında accepted var mı ona bakıyoruz, varsa hata çıkartıyoruz
        offers_id = self.env["estate.property.offer"].search([
            ("property_id", "=", self.property_id.id),
            ("status", "=", "accepted")
        ])

        if offers_id:
            raise ValidationError("You have an accepted offer already!")

    def extend_offer_deadline(self):
        active_ids = self._context.get("active_ids", []) # seçilenler veya şu an içinde bulunduğun active id ler oluyor
        if active_ids:
            offer_ids = self.env["estate.property.offer"].browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10

    def extend_offer_deadline2(self):
        pass
