from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mercyl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'products.views.home', name='home'),
    url(r'^aboutus$', 'products.views.aboutus', name='aboutus'),
    url(r'^contact', 'products.views.contact', name='contact'),
    url(r'^products/(?P<machinetype>[\w-]+)/$', 'products.views.list_machines', name='list_machines'),
    url(r'^product/(?P<slug>[\w-]+)/$', 'products.views.single', name='single'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)