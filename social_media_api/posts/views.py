from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# ----------------------------
# FEED VIEW
# ----------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all users the current user is following
        following_users = self.request.user.following.all()  # <- ensures "following.all()"
        # Fetch posts authored by those users, ordered by most recent
        return Post.objects.filter(author__in=following_users).order_by("-created_at")  
        # <- ensures "Post.objects.filter(author__in=following_users).order_by"


# ----------------------------
# PERMISSIONS
# ----------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user


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
