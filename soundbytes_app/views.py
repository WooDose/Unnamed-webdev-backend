
from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from soundbytes_app.serializers import SoundbyteSerializer
from soundbytes_app.models import Soundbyte

from notifications_app.serializers import NotificationSerializer
from notifications_app.models import Notification

from permissions_app.services import APIPermissionClassFactory

def eval(user, obj, request):
    return user.pk == obj.uploader.id


class SoundbyteViewSet(viewsets.ModelViewSet):
    queryset = Soundbyte.objects.all()
    serializer_class = SoundbyteSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='SoundbytePermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True,
                    'view_all': True
                },
                'instance': {
                    'retrieve': True,
                    'poster' : 'soundbytes_app.view_soundbyte',
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
        soundbyte = serializer.save(uploader = poster)
        assign_perm('soundbytes_app.view_soundbyte', user, soundbyte)
        return Response(serializer.data)

    @action(detail=True,  methods=['get'])
    def view_all(self, request, pk=None):
        all_soundbytes = []
        recent_soundbytes = Soundbyte.objects.filter().order_by('-upload_date')[:30][::-1]
        for soundbyte in recent_soundbytes:
            all_soundbytes.append(SoundbyteSerializer(soundbyte).data)
        return Response(all_soundbytes)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        soundbyte = self.get_object()
        self.add_like(soundbyte)
        return Response(SoundbyteSerializer(soundbyte).data)

    def add_like(self, soundbyte):
        soundbyte.likes += 1
        if soundbyte.likes % 1 == 0 and soundbyte.uploader is not None:
            recipient = soundbyte.uploader
            recipient_user = User.objects.filter(pk=recipient.pk)
            notification = Notification(recipient=recipient, notification_type='sbt_like')
            notification.save()
            assign_perm('notifications_app.view_notification', recipient_user, notification)
        soundbyte.save()      

    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        soundbyte = self.get_object()
        self.disable_soundbyte(soundbyte)
        return Response(SoundbyteSerializer(soundbyte).data)
    
    def disable_soundbyte(self, soundbyte):
        soundbyte.description = "This soundbyte has been disabled. However, it will forever be recorded in hisoundbyte that you at one point made this soundbyte."
        soundbyte.directory = '/src/img/disabled.png'
        soundbyte.save()

    @action(detail=True, methods=['patch'])
    def update_description(self, request, pk=None):
        soundbyte = self.get_object()
        soundbyte.description = request.data.get('new_description')
        soundbyte.save()
        return Response(SoundbyteSerializer(soundbyte).data)
