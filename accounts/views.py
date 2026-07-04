from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import RegisterSerializer, LoginSerializer

@api_view(["GET"])
def home(request):
    return Response({"Welcome to StackShop!!"})

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    refresh = RefreshToken.for_user(user)

    response = Response({"message":"Registered succesfully",
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

    response = Response({"message":"Login successful",
                         "access":str(refresh.access_token)}, status=status.HTTP_200_OK)

    response.set_cookie(key="refresh_token",
                        value=str(refresh),
                        httponly=True,
                        # secure=True,
                        samesite="Lax",
                        max_age=7*24*60*60)

    return response

