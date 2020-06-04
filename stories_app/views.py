
from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from stories_app.serializers import StorySerializer
from stories_app.models import Story

from notifications_app.serializers import NotificationSerializer
from notifications_app.models import Notification

from permissions_app.services import APIPermissionClassFactory

def eval(user, obj, request):
    return user.pk == obj.uploader.id


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='StoryPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True,
                    'view_all': True
                },
                'instance': {
                    'retrieve': True,
                    'poster' : 'stories_app.view_story',
                    'destroy' : eval,
                    'update_description' : eval,
                    'disable' : eval,
                    'view_all': True,
                }
            }
        ),
    )


    def perform_create(self, serializer):
        user = self.request.user
        poster = Poster.objects.get(pk=user.pk)
        story = serializer.save(uploader = poster)
        assign_perm('stories_app.view_story', user, story)
        return Response(serializer.data)

    @action(detail=True,  methods=['get'])
    def view_all(self, request, pk=None):
        all_stories = []
        recent_stories = Story.objects.filter().order_by('-upload_date')[:30][::-1]
        for story in recent_stories:
            all_stories.append(StorySerializer(story).data)
        return Response(all_stories)

        

    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        story = self.get_object()
        self.disable_story(story)
        return Response(StorySerializer(story).data)
    
    def disable_story(self, story):
        story.description = "This story has been disabled. However, it will forever be recorded in history that you at one point made this story."
        story.directory = '/src/img/disabled.png'
        story.save()

    @action(detail=True, methods=['patch'])
    def update_description(self, request, pk=None):
        story = self.get_object()
        story.description = request.data.get('new_description')
        story.save()
        return Response(StorySerializer(story).data)
