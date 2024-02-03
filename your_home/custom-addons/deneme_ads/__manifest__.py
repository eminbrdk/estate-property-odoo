{
    'name': 'Your Module Name 3',
    'version': '1.0',
    'category': 'Your Category',
    'summary': 'Eminin öğrenme modülüdür',
    'author': 'Muhammed Emin Bardakcı',
    'depends': ["base", "mail"],
    'data': [
        # Security Files
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',

        # View Fiels
        'views/property_view.xml',
        'views/property_type_view.xml',
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        'views/menu_items.xml',

        # Web Fiels
        'views/property_web_template.xml',
        'views/create_property_tag.xml',
        
        # Data Files
        "data/property_type.xml",
        "data/mail_template.xml",

        # Report
        "report/report_template.xml",
        "report/property_report.xml",
    ],
    "demo": [
        "demo/property_tag.xml"
    ],
    "assets": {
        'web.assets_backend': [
            #'deneme_ads/static/src/js/my_custom_tag.js',
            'deneme_ads/static/src/xml/my_custom_tag.xml',
        ]
    },
    'installable': True,
    'license': 'LGPL-3',
}