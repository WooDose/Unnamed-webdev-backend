from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

#from collections_app.models import Collection
#from collections_app.serializers import CollectionSerializer

from images_app.models import Image
from images_app.serializers import ImageSerializer

from links_app.models import Link
from links_app.serializers import LinkSerializer

from messages_app.models import Message
from messages_app.serializers import MessageSerializer

from notifications_app.models import Notification
from notifications_app.serializers import NotificationSerializer

from soundbytes_app.models import Soundbyte
from soundbytes_app.serializers import SoundbyteSerializer

from stories_app.models import Story
from stories_app.serializers import StorySerializer

from videos_app.models import Video
from videos_app.serializers import VideoSerializer

from permissions_app.services import APIPermissionClassFactory
# Create your views here.

def eval_message(user, obj, request):
    return user.pk == obj.id

class PosterViewSet(viewsets.ModelViewSet):
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='PosterPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True
                },
                'instance': {
                    'retrieve': 'posters_app.view_poster',
                    'images' : 'posters_app.view_poster',
                    'links' : 'posters_app.view_poster',
                    'messages' : eval_message,
                    'notifications' : eval_message,
                    'soundbytes' : 'posters_app.view_poster',
                    'stories' : 'posters_app.view_poster',
                    'videos' : 'posters_app.view_poster',
                }
            }
        ),
    )



    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        poster = self.get_object()
        poster_images = []
        for image in Image.objects.filter(uploader=poster):
            poster_images.append(ImageSerializer(image).data)
        return Response(poster_images)

    @action(detail=True, methods=['get'])
    def links(self, request, pk=None):
        poster = self.get_object()
        poster_links = []
        for link in Link.objects.filter(uploader=poster):
            poster_links.append(LinkSerializer(link).data)
        return Response(poster_links)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        user = self.request.user
        poster = self.get_object()
        poster_messages = []
        for message in Message.objects.filter(recipient=user.pk):
            poster_messages.append(MessageSerializer(message).data)
        return Response(poster_messages)

    @action(detail=True, methods=['get'])
    def notifications(self, request, pk=None):
        poster = self.get_object()
        poster_notifications = []
        for image in Notification.objects.filter(recipient=poster):
            poster_notifications.append(NotificationSerializer(image).data)
        return Response(poster_notifications)        

    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        poster = self.get_object()
        poster_stories = []
        for image in Story.objects.filter(recipient=poster):
            poster_stories.append(StorySerializer(image).data)
        return Response(poster_stories)        

    @action(detail=True, methods=['get'])
    def soundbytes(self, request, pk=None):
        poster = self.get_object()
        poster_soundbytes = []
        for image in Soundbyte.objects.filter(recipient=poster):
            poster_soundbytes.append(SoundbyteSerializer(image).data)
        return Response(poster_soundbytes)        

    @action(detail=True, methods=['get'])
    def videos(self, request, pk=None):
        poster = self.get_object()
        poster_videos = []
        for image in Video.objects.filter(recipient=poster):
            poster_videos.append(VideoSerializer(image).data)
        return Response(poster_videos)        