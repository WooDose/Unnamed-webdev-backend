from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from notes_app.serializers import NoteSerializer
from notes_app.models import Note

from permissions_app.services import APIPermissionClassFactory
# Create your views here.

def eval(user, obj, request):
    return user.pk == obj.uploader.id


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='NotePermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True
                },
                'instance': {
                    'retrieve': 'notes_app.view_note',
                    'poster' : 'notes_app.view_note',
                    'destroy' : eval,
                    'update_content' : eval,
                    'like' : 'notes_app.view_note',
                    'disable' : eval,
                    'view_all' : True
                }
            }
        ),
    )


    def perform_create(self, serializer):
        user = self.request.user
        poster = Poster.objects.get(pk=user.pk)
        note = serializer.save(uploader = poster)
        assign_perm('notes_app.view_note', user, note)
        return Response(serializer.data)

    @action(detail=True,  methods=['get'])
    def view_all(self, request, pk=None):
        all_notes = []
        recent_notes = Note.objects.filter().order_by('-upload_date')[:30][::-1]
        for note in recent_notes:
            all_notes.append(NoteSerializer(note).data)
        return Response(all_notes)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        note = self.get_object()
        self.add_like(note)
        return Response(NoteSerializer(note).data)

    def add_like(self, note):
        note.likes += 1
        note.save()


    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        note = self.get_object()
        self.disable_note(note)
        return Response(NoteSerializer(note).data)
    
    def disable_note(self, note):
        note.caption = "This note has been disabled. However, it will forever be recorded in history that you at one point made this note."
        note.url = ''
        note.save()

    @action(detail=True, methods=['patch'])
    def update_content(self, request, pk=None):
        note = self.get_object()
        note.contents = request.data.get('new_content')
        note.save()
        return Response(NoteSerializer(note).data)

    @action(detail=True, methods=['patch'])
    def update_title(self, request, pk=None):
        note = self.get_object()
        note.title = request.data.get('new_title')
        note.save()
        return Response(NoteSerializer(note).data)
