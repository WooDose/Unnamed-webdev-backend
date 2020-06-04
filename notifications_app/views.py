from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from notifications_app.serializers import NotificationSerializer
from notifications_app.models import Notification

from permissions_app.services import APIPermissionClassFactory

def eval(user, obj, request):
    return user.pk == obj.recipient.id


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='NotificationPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True,
                },
                'instance': {
                    'destroy' : eval,
                    'delete' : eval,
                }
            }
        ),
    )

## They can only be read through the correct user's "Notifications" method.
## Notifications can only be created through other means; such as every time a user's post reaches n likes.
## However, they will be deleted on read.
    @action(detail=True,  methods=['delete'])
    def delete(self, request, pk=None):
        notification = self.get_object()
        notification.delete()
        return Response
   