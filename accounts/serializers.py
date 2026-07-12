from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["email", "username", "password", "phone_no"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_phone_no(self, value):
        if User.objects.filter(phone_no=value).exists():
            raise serializers.ValidationError("Phone No. already exists")

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Email and password are required."
            )

        user = authenticate(username=email,
                            password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        attrs["user"] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_no",
            "profile_picture",
            "is_verified",
            "date_joined",
            "updated_at"
        ]

        read_only_fields = [
            "id",
            "is_verified",
            "date_joined",
            "updated_at"
        ]

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_phone_no(self, value):
        user = self.instance
        if User.objects.filter(phone_no=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Phone No. already exists")
        return value

    def validate_username(self, value):
        user = self.instance
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_profile_picture(self, value):
        if value.size > 2*1024*1024:
            raise serializers.ValidationError("Image should be less than 2 MB")

        if value.content_type not in [
            "image/jpeg",
            "image/png"
        ]:
            raise serializers.ValidationError("Only jpeg/png are allowed")

        return value


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["new_password"]:
            raise serializers.ValidationError("password do not match")

        return attrs
