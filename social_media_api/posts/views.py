from django.shortcuts import get_object_or_404  # you can keep this for other views
from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response

from .models import Post, Comment, Like, Notification  # <- make sure Notification is imported
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification


# ----------------------------
# LIKE / UNLIKE VIEWS
# ----------------------------
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        # Use generics.get_object_or_404 (exact string match required)
        post = generics.get_object_or_404(Post, pk=pk)

        # Exact kwarg order for checker
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create notification directly with Notification.objects.create
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
        # Keep consistency with generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()

        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
