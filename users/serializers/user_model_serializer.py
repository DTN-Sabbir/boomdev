from rest_framework import serializers
from users.models import CustomUser


class UserModelCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate_email(self, value):
        """Validate email and raise custom error code if invalid."""
        if not value or "@" not in value:
            raise serializers.ValidationError(
                {"error_code": 101, "detail": "Invalid email address"}
            )
        return value

    def validate_role(self, value):
        """Validate role and raise custom error code if invalid."""
        valid_roles = [
            CustomUser.Roles.ADMIN,
            CustomUser.Roles.MANAGER,
            CustomUser.Roles.USER,
        ]
        if value not in valid_roles:
            raise serializers.ValidationError(
                {"error_code": 102, "detail": "Invalid role"}
            )
        return value

    def create(self, validated_data):
        # Extract fields with defaults if missing
        email = validated_data.get("email")
        password = validated_data.get("password")
        name = validated_data.get("name")
        role = validated_data.get("role", "User")
        if role is None:
            raise serializers.ValidationError({"role": "This field is required."})

        # Create user
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            name=name,
            role=role,
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "email",
            "role",
            "is_active",
            "is_staff",
            "date_joined",
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "email",
            "role",
            "is_active",
            "is_staff",
            "date_joined",
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "email",
            "role",
            "is_active",
            "is_staff",
            "date_joined",
        ]


class UserModelDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id"]
