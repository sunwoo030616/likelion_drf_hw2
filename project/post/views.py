from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .serializers import PostSerializer, CommentSerializer, PostListSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer
    
    def get_permissions(self):
        if self.action in ["create", "update", "destroy", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        post.like_count = post.likes.count()
        post.save()

        return Response({'like_count': post.like_count})
    
    @action(methods=['GET'], detail=False)
    def top_three_likes(self, request):
        top_posts = self.get_queryset().order_by('-like_count')[:3]
        serializer = PostSerializer(top_posts, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []
    
    def get_object(self):
        obj = super.get_object()
        return obj

class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset

    # def list(self, request, movie_id=None):
    #     movie = get_object_or_404(Movie, id=movie_id)
    #     queryset = self.filter_queryset(self.get_queryset().filter(movie=movie))
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)