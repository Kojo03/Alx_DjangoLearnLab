from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets, permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification


# ----------------------------
# Custom Permission
# ----------------------------
class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object
    to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for anyone
        if request.method in SAFE_METHODS:
            return True
        # Write/delete only if the user is the author
        return obj.author == request.user


# ----------------------------
# LIKE / UNLIKE VIEWS
# ----------------------------
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
            )

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()

        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)


# ----------------------------
# FEED VIEW
# ----------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


# ----------------------------
# CRUD VIEWSETS
# ----------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
