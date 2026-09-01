"""
URL configuration for matchsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Google login lives here
    path('', include('accounts.urls')),
    path('', include('matching.urls')),
    path('chat/', include('chat.urls')),
]


# Serve uploaded photos (profile_photos/...) even when DEBUG=False.
# This isn't the ideal setup for a large, high-traffic site (a proper
# production build would use S3/Cloudinary + a CDN), but for a small
# free-tier deployment it's the only way the photos show up at all —
# without this line, every uploaded photo returns 404 as soon as
# DEBUG is turned off for production.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

