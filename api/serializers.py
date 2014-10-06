from rest_framework import serializers
from django.contrib.auth.models import User
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from webcams.models import Webcam
from sponsors.models import Sponsor
from social_media.models import SocialMedia
from .fields import APIImageField, ProjectActiveField

class WebcamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webcam
        fields = ('id', 'name', 'url', )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined', )

class RoboUserSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()

    # TODO: find better way to do this
    def to_native(self, obj):
        """
        Hack to embed 'user' fields into main object
        eliminating nested fields.
        """

        ret = super(RoboUserSerializer, self).to_native(obj)
        p_serializer = UserSerializer(obj.user, context=self.context)
        p_ret = p_serializer.to_native(obj.user)

        # If user ID exists, delete it from dictionary
        # because only interested in RoboUser id
        if 'id' in p_ret:
            del p_ret['id']

        for key in p_ret:
            ret[key] = p_ret[key]

        if 'user' in p_ret:
            del ret['user']

        return ret

    class Meta:
        model = RoboUser
        depth = 2

        fields = ('id', )

class ProjectSerializer(serializers.ModelSerializer):
    image = APIImageField(source='image')
    active = ProjectActiveField(source='last_api_activity')

    class Meta:
        model = Project
        fields = ('id', 'name', 'image', 'blurb', 'description', 'website', 'display', 'leaders', 'active', 'last_api_activity', )

class OfficerSerializer(serializers.ModelSerializer):
    image = APIImageField(source='image')

    class Meta:
        model = Officer
        fields = ('id', 'position', 'user', 'image', 'description', 'order', )

class SponsorSerializer(serializers.ModelSerializer):
    logo = APIImageField(source='logo')

    class Meta:
        model = Sponsor
        fields = ('id', 'name', 'logo', 'website', 'active', 'order', )

class SocialMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialMedia
        fields = ('id', 'name', 'url', 'order', )
