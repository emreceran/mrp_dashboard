{
    'name': 'MRP Dashboard - Üretim Yönetimi',
    'version': '1.0',
    'summary': 'Üretim Emirleri için Timeline ve Gelişmiş Dashboard Özellikleri',
    'description': 'Nakış, üretim, sevkiyat ve montaj özetlerini içeren Yönetim ekranı.',
    'category': 'Manufacturing/Manufacturing',
    'author': 'Senin Adın/Şirketin',
    # 'project' modülünü ekledik:
    'depends': ['mrp', 'web_timeline', 'project', 'yuz18'],
    'data': [
        'views/mrp_production_views.xml',
        'views/management_views.xml',
        'views/product_views.xml',

    ],

    # CSS dosyamızı backend arayüzüne ekliyoruz:
    'assets': {
        'web.assets_backend': [
            'mrp_dashboard/static/src/css/dashboard.css',
        ],
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}