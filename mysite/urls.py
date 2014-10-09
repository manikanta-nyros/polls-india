from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^',include('polls.urls',namespace="polls")),
    url(r'^',include('registration.backends.default.urls')),
    url(r'^',include('registration.auth_urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/',include('django.contrib.flatpages.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace ='auth')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^search/', include('haystack.urls')),
    
)
