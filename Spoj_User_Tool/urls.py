from django.conf.urls.defaults import *
from Spoj_User_Tool.views import home, single_user, multi_user
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', home),
	url(r'^user/([a-z]{1}[a-z0-9_]{2,})$', single_user),
	url(r'^user/([a-z]{1}[a-z0-9_]{2,})/([a-z]{1}[a-z0-9_]{2,})$', multi_user),
    # Examples:
    # url(r'^$', 'Spoj_User_Tool.views.home', name='home'),
    # url(r'^Spoj_User_Tool/', include('Spoj_User_Tool.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
