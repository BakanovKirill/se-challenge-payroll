from __future__ import unicode_literals, absolute_import

import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import include
from django.contrib import admin

from rest_framework import routers

from .views import (
    landing,
    FileUploadView
)

router = routers.DefaultRouter()
# router.register(r'^profiles', ProfileViewSet, 'profiles')

urlpatterns = \
    [
        # Third-paty views
        path('admin/', admin.site.urls),
        path('__debug__/', include(debug_toolbar.urls)),

        # Landing page
        path('', landing, name='landing'),
        path('upload_report/', FileUploadView.as_view(), name='upload_report'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static('/coverage/', document_root=settings.COVERAGE_ROOT)
