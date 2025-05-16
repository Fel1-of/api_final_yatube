from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly)
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Follow, Group, Post, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'pub_date']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('title',)
    search_fields = ('title',)


class FollowViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.CreateModelMixin):
    http_method_names = ['get', 'post']
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
