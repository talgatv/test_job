from .models import Profile
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from rest_framework import serializers, status
from PIL import Image, ImageDraw
import pathlib

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'photo',
            'gender',
            )

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
        image = Image.open(profile_data['photo'].file).convert("RGBA")
        drawing = ImageDraw.Draw(image)
        drawing.text((0, 0), "whatemark", fill='black')
        adress = settings.MEDIA_ROOT +  '/users/user_{0}/'.format(user.id)
        pathlib.Path(adress).mkdir(parents=True, exist_ok=True)
        image.save(adress + str(profile_data['photo'])  )
        Profile.objects.filter(user = user).update(
            photo=settings.MEDIA_URL + 'users/user_{0}/{1}'.format(
                user.id,
                profile_data['photo']
                )
            )


        return user
