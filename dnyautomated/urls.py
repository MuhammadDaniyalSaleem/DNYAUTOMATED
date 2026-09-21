from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns=[path('admin/',admin.site.urls),path('',include('agency.urls')),path('robots.txt',TemplateView.as_view(template_name='agency/robots.txt',content_type='text/plain'))]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
handler404='agency.error_views.error_404'; handler500='agency.error_views.error_500'
