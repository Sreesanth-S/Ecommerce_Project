from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializer import RegisterSerializer, LoginSerializer, UserProfileSerializer

@api_view(["GET"])
def home(request):
    return Response({"message":"welcome to StackShop API!!"})

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
                        # secure=True,
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
                        # secure=True,
                        samesite="Lax",
                        max_age=7*24*60*60)

    return response


@api_view(["GET","PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response({"user":serializer.data})

    if request.method == "PUT":
        serializer = UserProfileSerializer(request.user, data=request.data)
    else:
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response({"message":"profile updated successfully",
                     "user":serializer.data}, status=status.HTTP_200_OK)


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
                            # secure=True,
                            samesite="Lax",
                            max_age=7*24*60*60)
    return response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response({"message":"logged out successfully"})

    response.delete_cookie("refresh_token")
    
    return response
