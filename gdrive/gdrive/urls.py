from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gdrive.views.home', name='home'),
    # url(r'^gdrive/', include('gdrive.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^add_account$', 'gdoauth2.views.add_account',
        name='gdoauth2_add_account'),
    url(r'^oauth2callback$', 'gdoauth2.views.callback',
        name='gdoauth2_callback'),
)
