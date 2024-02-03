odoo.define("deneme_ads.CustomAction", function(require) {
    "use strict";

    var AbstractAction = require("web.AbstractAction");
    var core = require("web.core");

    var CustomAction = AbstractAction.extend({
        template: "qmk", // my_custom_tag.xml den aldım
        start: function() {
            console.log("Action")
        }
    })

    core.action_registry.add("custom_client_action_tag", CustomAction) // custom_client_action_tag, client action'un yaratıldığı recorda da yazan tag

});