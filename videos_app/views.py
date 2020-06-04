
from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from videos_app.serializers import VideoSerializer
from videos_app.models import Video

from notifications_app.serializers import NotificationSerializer
from notifications_app.models import Notification

from permissions_app.services import APIPermissionClassFactory

def eval(user, obj, request):
    return user.pk == obj.uploader.id


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='VideoPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True,
                    'view_all': True
                },
                'instance': {
                    'retrieve': True,
                    'poster' : 'videos_app.view_video',
                    'destroy' : eval,
                    'update_description' : eval,
                    'disable' : eval,
                    'like' : True,
                    'view_all': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        user = self.request.user
        poster = Poster.objects.get(pk=user.pk)
        video = serializer.save(uploader = poster)
        assign_perm('videos_app.view_video', user, video)
        return Response(serializer.data)

    @action(detail=True,  methods=['get'])
    def view_all(self, request, pk=None):
        all_videos = []
        recent_videos = Video.objects.filter().order_by('-upload_date')[:30][::-1]
        for video in recent_videos:
            all_videos.append(VideoSerializer(video).data)
        return Response(all_videos)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        video = self.get_object()
        self.add_like(video)
        return Response(VideoSerializer(video).data)

    def add_like(self, video):
        video.likes += 1
        if video.likes % 1 == 0 and video.uploader is not None:
            recipient = video.uploader
            recipient_user = User.objects.filter(pk=recipient.pk)
            notification = Notification(recipient=recipient, notification_type='vid_like')
            notification.save()
            assign_perm('notifications_app.view_notification', recipient_user, notification)
        video.save()      

    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        video = self.get_object()
        self.disable_video(video)
        return Response(VideoSerializer(video).data)
    
    def disable_video(self, video):
        video.caption = "This video has been disabled. However, it will forever be recorded in hivideo that you at one point made this video."
        video.directory = '/src/img/disabled.png'
        video.save()

    @action(detail=True, methods=['patch'])
    def update_description(self, request, pk=None):
        video = self.get_object()
        video.caption = request.data.get('new_description')
        video.save()
        return Response(VideoSerializer(video).data)
