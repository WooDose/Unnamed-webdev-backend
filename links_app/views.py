from django.shortcuts import render
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posters_app.serializers import PosterSerializer
from posters_app.models import Poster

from links_app.serializers import LinkSerializer
from links_app.models import Link

from permissions_app.services import APIPermissionClassFactory
# Create your views here.

def eval(user, obj, request):
    return user.pk == obj.uploader.id


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='LinkPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'create_auth': True
                },
                'instance': {
                    'retrieve': 'links_app.view_link',
                    'poster' : 'links_app.view_link',
                    'destroy' : eval,
                    'update_caption' : eval,
                    'like' : 'links_app.view_link',
                    'disable' : eval,
                    'view_all' : True
                }
            }
        ),
    )


    def perform_create(self, serializer):
        user = self.request.user
        poster = Poster.objects.get(pk=user.pk)
        link = serializer.save(uploader = poster)
        assign_perm('links_app.view_link', user, link)
        return Response(serializer.data)

    @action(detail=True,  methods=['get'])
    def view_all(self, request, pk=None):
        all_links = []
        recent_links = Link.objects.filter().order_by('-upload_date')[:30][::-1]
        for link in recent_links:
            all_links.append(LinkSerializer(link).data)
        return Response(all_links)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        link = self.get_object()
        self.add_like(link)
        return Response(LinkSerializer(link).data)

    def add_like(self, link):
        link.likes += 1
        link.save()


    @action(detail=True, methods=['patch'])
    def disable(self, request, pk=None):
        link = self.get_object()
        self.disable_link(link)
        return Response(LinkSerializer(link).data)
    
    def disable_link(self, link):
        link.caption = "This link has been disabled. However, it will forever be recorded in history that you at one point made this link."
        link.url = ''
        link.save()

    @action(detail=True, methods=['patch'])
    def update_caption(self, request, pk=None):
        link = self.get_object()
        link.caption = request.data.get('new_caption')
        link.save()
        return Response(LinkSerializer(link).data)
