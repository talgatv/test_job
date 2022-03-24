from .models import Profile
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1


class ProfileCreateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'profile',
            )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.get_or_create(user = user)
        Profile.objects.filter(user = user).update(**profile_data)
        return user
