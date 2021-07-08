from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('review.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]