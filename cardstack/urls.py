from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from cardstack import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cardstack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main, name='main'),
    url(r'^spending/', views.spending, name='spending'),
    url(r'^get_data/', views.ajax_get_data),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

