{
    'name': 'Odoo Twilio SMS Connector',
    'version': '12.0.0.0.1',
    'category': 'SMS',
    'description': """
* Testing SMS
    """,
    'website': 'https://www.alvinadjie.blogspot.com',
    'depends': ['base_setup', 'sale'],
    'data': [
        
        'views/sale_view.xml',
        'views/twillio_config.xml',
        'views/res_company_views.xml',
        
    ],
    "external_dependencies": {
        'python': ['twilio']
    },
    'installable': True,
}