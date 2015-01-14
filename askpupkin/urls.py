from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('ask.views',
    url(r'^$', 'index_latest', name='index_latest'),
    url(r'^new/$', 'index_latest', name='index_latest'),
    url(r'^popular/$', 'index_popular', name='index_popular'),
    url(r'^question/$', 'answers', name='answers'),
    url(r'^tag/$', 'tag', name='tag'),
    url(r'^user/$', 'user', name='user'),
    url(r'^search/$', 'search', name='search'),
    url(r'^rating/$', 'rating', name='rating'),
    url(r'^mark/$', 'mark', name='mark'),
    url(r'^register/$', 'register', name='register'),
    url(r'^statistics/$', 'statistics', name='statistics'),
    url(r'^chart/$', 'chart', name='chart'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
