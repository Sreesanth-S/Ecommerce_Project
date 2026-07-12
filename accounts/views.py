from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    refresh = RefreshToken.for_user(user)

    response = Response({"message":"registered succesfully",
                         "user":UserProfileSerializer(user).data,
                         "access":str(refresh.access_token)}, status=status.HTTP_201_CREATED)

    response.set_cookie(key="refresh_token",
                        value=str(refresh),
                        httponly=True,
                        secure=settings.JWT_COOKIE_SECURE,
                        samesite="Lax",
                        max_age=7*24*60*60)

    return response


@api_view(["POST"])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data["user"]

    refresh = RefreshToken.for_user(user)

    response = Response({"message":"login successful",
                         "user":UserProfileSerializer(user).data,
                         "access":str(refresh.access_token)}, status=status.HTTP_200_OK)

    response.set_cookie(key="refresh_token",
                        value=str(refresh),
                        httponly=True,
                        secure=settings.JWT_COOKIE_SECURE,
                        samesite="Lax",
                        max_age=7*24*60*60)

    return response


@api_view(["GET","PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response({"user":serializer.data}, status=status.HTTP_200_OK)

    serializer = UserProfileSerializer(request.user, data=request.data, partial=(request.method == "PATCH"))

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({"message":"profile updated successfully",
                     "user":serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    user = request.user

    if not user.check_password(serializer.validated_data["old_password"]):
        return Response({"detail":"old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data["new_password"])
    user.save()

    return Response({"message":"password updated successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response({"message":"logged out successfully"}, status=status.HTTP_200_OK)

    response.delete_cookie("refresh_token")

    return response


@api_view(["POST"])
def refresh_token(request):
    token = request.COOKIES.get("refresh_token")

    if not token:
        return Response({"detail":"refresh token not found"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = TokenRefreshSerializer(data={"refresh":token})

    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    response = Response({"access_token":data.get("access")}, status=status.HTTP_200_OK)

    if "refresh" in data:
        response.set_cookie(key="refresh_token",
                            value=data.get("refresh"),
                            httponly=True,
                            secure=settings.JWT_COKIE_SECURE,
                            samesite="Lax",
                            max_age=7*24*60*60)
    return response
