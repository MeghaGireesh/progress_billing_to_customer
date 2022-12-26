{
    'name': "Progress Billing",
    'version': '16.0.1.0.0',
    'summary': """ Progress Billing To Customer""",
    'description': 'Progress Billing To Customer',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'account'],

    'data': [
        'reports/process_billing_pdf.xml',
        'views/anlytic_account_inherit_views.xml',
        'views/invoice_inherit_views.xml',
    ],
    # 'license': 'AGPL-3',
    'installable': True,
    'application': False,
}