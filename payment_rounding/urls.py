from django.contrib import admin
from django.urls import path, include


handler404 = 'api.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api'))
]
