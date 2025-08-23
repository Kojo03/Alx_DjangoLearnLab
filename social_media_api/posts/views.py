from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.utils import create_notification


# ----------------------------
# PERMISSIONS
# ----------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow safe methods for everyone, but restrict edit/delete to owner."""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user


# ----------------------------
# FEED VIEW
# ----------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all users the current user is following
        following_users = self.request.user.following.all()
        # Fetch posts authored by those users, ordered by most recent
        return Post.objects.filter(author__in=following_users).order_by("-created_at")


# ----------------------------
# POST VIEWSET
# ----------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ["author__username"]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ----------------------------
# COMMENT VIEWSET
# ----------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ----------------------------
# LIKE / UNLIKE VIEWS
# ----------------------------
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Prevent duplicate like
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create notification for post author
        if post.author != request.user:
            create_notification(
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
