from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from . import views
from utils.watermark import WaterMarkView

from landing.SignalHandlers import return_view, cancel_view, paypal_sandbox
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticSitemap, ProductSitemap


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('landing.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('admin.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'', include('product.urls')),

    url(r'watermark/', WaterMarkView.as_view(), name='watermark'),


    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^paypal_sandbox/', paypal_sandbox, name='paypal_sandbox'),
    url(r'^return_url/', return_view, name='return_url' ),
    url(r'^cancel_url/', cancel_view, name='cancel_url'),

]

# # 404, 500 handlers
# urlpatterns += [
#     url(r'^404/$', views.handler404),
#     url(r'^500/$', views.handler500),
# ]

# api
urlpatterns += [
    # url(r'', include('product.api.urls')),
]

# sitemap
sitemaps = {
 'pages': StaticSitemap,
 'products': ProductSitemap
}
urlpatterns += [
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps})
]

if settings.DEBUG:
    def trigger_error(request):
        division_by_zero = 1 / 0
    urlpatterns += [
        url('^sentry-debug/$', trigger_error),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
