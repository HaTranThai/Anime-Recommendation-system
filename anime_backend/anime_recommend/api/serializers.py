# api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import Anime, UserProfile, UserWatchHistory

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'full_name', 'phone_number', 'age', 'gender')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'roles': ['customer'],
            'user_id': user.id,
            'full_name': user.full_name,
        })
        return data


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    watched_animes = AnimeSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'watched_animes']

class UserWatchHistorySerializer(serializers.ModelSerializer):
    anime = AnimeSerializer(read_only=True)

    class Meta:
        model = UserWatchHistory
        fields = ['id', 'anime', 'last_watched', 'progress']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu cũ không chính xác.")
        return value

    def validate(self, data):
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError("Mật khẩu mới phải khác mật khẩu cũ.")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
