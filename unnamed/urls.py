"""unnamed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)


from posters_app.views import PosterViewSet
from images_app.views import ImageViewSet
from links_app.views import LinkViewSet
from messages_app.views import MessageViewSet
from notes_app.views import NoteViewSet
from stories_app.views import StoryViewSet
from soundbytes_app.views import SoundbyteViewSet
from videos_app.views import VideoViewSet

router = routers.DefaultRouter()

router.register(r'poster', PosterViewSet)
router.register(r'image', ImageViewSet)
router.register(r'link', LinkViewSet)
router.register(r'message', MessageViewSet)
router.register(r'note', NoteViewSet)
router.register(r'story', StoryViewSet)
router.register(r'soundbyte', SoundbyteViewSet)
router.register(r'video', VideoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
        url(r'^api-auth/', include('rest_framework.urls')),
        url(r'^api/v1/', include(router.urls)),
        url(r'^api/v1/token-auth/', obtain_jwt_token),
        url(r'^api/v1/token-refresh/', refresh_jwt_token),
]