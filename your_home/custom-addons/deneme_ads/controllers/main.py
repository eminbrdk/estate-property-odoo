from odoo import http
from odoo.http import request

# class belirleyip içine (PropertyController) yazarsan ve
# import odoo.addons.deneme_ads.controllers.main import PropertyController yaparsan
# farklı modullerde bunu böyle kullanabilirim.


class PropertyController(http.Controller):

    @http.route(["/properties"], type="http", auth="public", website=True)
    def show_properties(self):
        # sudo eklersek giriş yapmadanda websitesine erişilebilecek.
        property_tags = request.env["estate.property.tag"].sudo().search([])
        print(property_tags)
        return request.render("deneme_ads.property_list", {"property_tags": property_tags})

    # chatgpt yaptı
    @http.route("/properties/create", type="http", auth="public", website=True, methods=["GET", "POST"])
    def create_property_tag(self, **post):
        if request.httprequest.method == "POST":
            # Validate input data
            name = post.get("name")
            color = post.get("color")
            if not name or not color:
                return request.redirect("/properties")  # Redirect to the properties page with an error message

            # Create a new property tag
            request.env["estate.property.tag"].sudo().create({"name": name, "color": color})

            return request.redirect("/properties")  # Redirect to the properties page after successful creation

        return request.render("deneme_ads.property_form")