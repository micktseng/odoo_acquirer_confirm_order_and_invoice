# -*- coding: utf-8 -*-
{
    'name': "Acquirer Confirm Order And Invoice",

    'summary': "",

    'description': "",

    'author': "Mick",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'portal_sale',
        'website_portal',
        'website_payment'
    ],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [],
}