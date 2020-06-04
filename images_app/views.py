from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from images_app.serializers import ImageSerializer
from images_app.models import Image

from notifications_app.serializers import NotificationSerializer
from notifications_app.models import Notification

from permissions_app.services import APIPermissionClassFactory

def eval(user, obj, request):
    return user.pk == obj.uploader.id


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ImagePermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True,
                    'view_all': True
                },
                'instance': {
                    'retrieve': True,
                    'poster' : 'images_app.view_image',
                    'destroy' : eval,
                    'update_caption' : eval,
                    'like' : 'images_app.view_image',
                    'disable' : eval,
                    'view_all': True,
                }
            }
        ),
    )


    def perform_create(self, serializer):
        user = self.request.user
        poster = Poster.objects.get(pk=user.pk)
        image = serializer.save(uploader = poster)
        assign_perm('images_app.view_image', user, image)
        return Response(serializer.data)

    @action(detail=True,  methods=['get'])
    def view_all(self, request, pk=None):
        all_images = []
        recent_images = Image.objects.filter().order_by('-upload_date')[:30][::-1]
        for image in recent_images:
            all_images.append(ImageSerializer(image).data)
        return Response(all_images)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        image = self.get_object()
        self.add_like(image)
        return Response(ImageSerializer(image).data)

    def add_like(self, image):
        image.likes += 1
        if image.likes % 1 == 0 and image.uploader is not None:
            recipient = image.uploader
            recipient_user = User.objects.filter(pk=recipient.pk)
            notification = Notification(recipient=recipient, notification_type='img_like')
            notification.save()
            assign_perm('notifications_app.view_notification', recipient_user, notification)
        image.save()
        

    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        image = self.get_object()
        self.disable_image(image)
        return Response(ImageSerializer(image).data)
    
    def disable_image(self, image):
        image.caption = "This image has been disabled. However, it will forever be recorded in history that you at one point made this image."
        image.directory = '/src/img/disabled.png'
        image.save()

    @action(detail=True, methods=['patch'])
    def update_caption(self, request, pk=None):
        image = self.get_object()
        image.caption = request.data.get('new_caption')
        image.save()
        return Response(ImageSerializer(image).data)
