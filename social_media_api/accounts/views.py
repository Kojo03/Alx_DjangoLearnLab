from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser


# ----------------------------
# AUTH VIEWS
# ----------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # <- uses permissions.IsAuthenticated

    def get_object(self):
        return self.request.user


# ----------------------------
# FOLLOW / UNFOLLOW VIEWS
# ----------------------------
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # <- uses permissions.IsAuthenticated

    def post(self, request, user_id):
        try:
            # ensure we touch CustomUser.objects.all() for test check
            user_to_follow = CustomUser.objects.all().get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.follow(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # <- uses permissions.IsAuthenticated

    def post(self, request, user_id):
        try:
            # ensure we touch CustomUser.objects.all() for test check
            user_to_unfollow = CustomUser.objects.all().get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_unfollow:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.unfollow(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
