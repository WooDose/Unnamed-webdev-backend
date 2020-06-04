from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from messages_app.serializers import MessageSerializer
from messages_app.models import Message

from permissions_app.services import APIPermissionClassFactory

def eval(user, obj, request):
    return user.pk == obj.recipient.id


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='MessagePermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True,
                },
                'instance': {
                    'retrieve': eval,
                    'destroy' : eval,
                    'delete' : eval,
                }
            }
        ),
    )


    def perform_create(self, serializer):
        recipient = self.request.data.get('recipient')
        recipient = Poster.objects.get(pk=recipient)
        recipient_user = User.objects.filter(pk=recipient.pk)
        message = serializer.save(recipient = recipient)
        assign_perm('messages_app.view_message', recipient_user, message)
        return Response(serializer.data)

    @action(detail=True,  methods=['delete'])
    def delete(self, request, pk=None):
        message = self.get_object()
        message.delete()
        return Response
   