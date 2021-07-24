# -*- coding: utf-8 -*-

{
    "name" : "Cancel POS Order",
    "author": "Edge Technologies",
    "version" : "14.0.1.0",
    "live_test_url":'https://youtu.be/lvFq1TzeTg4',
    "images":["static/description/main_screenshot.png"],
    'summary': 'pos cancel order for pos order cancel pos order cancel point of sale order cancel order from pos order cancel delete pos order delete cancel point of sale order point of sale cancel order for point of sales cancel order delete order from pos delete order',
    "description": """ This app used to cancel the order, invoice and stock.     

     """,
    "license" : "OPL-1",
    "depends" : ['base','point_of_sale'],
    "data": [
        'security/ir.model.access.csv',
        'views/pos_config_inherit.xml',
        'wizard/cancel_order.xml',
    ],
    'qweb': [
    ],
    "auto_install": False,
    "installable": True,
    "price": 18,
    "currency": 'EUR',
    "category" : "Point of Sale",
    
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
