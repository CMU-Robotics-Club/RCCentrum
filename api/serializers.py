from rest_framework import serializers
from django.contrib.auth.models import User
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer
from webcams.models import Webcam
from sponsors.models import Sponsor
from social_media.models import SocialMedia
from channels.models import Channel
from faq.models import Category, QA
from tshirts.models import TShirt
from .fields import APIImageField, ProjectActiveField

class WebcamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webcam
        fields = ('id', 'name', 'url', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_active',)


class RoboUserSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()

    magnetic = serializers.Field(source='is_magnetic_set')
    rfid = serializers.Field(source='is_rfid_set')
    machines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # TODO: find better way to do this
    def to_native(self, obj):
        """
        Hack to embed 'user' fields into main object
        eliminating nested fields.
        """

        if obj is None:
            return {}

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

        fields = ('id', 'magnetic', 'rfid', 'machines', )


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

class ChannelSerializer(serializers.ModelSerializer):
    active = serializers.Field(source='active')
    name = serializers.CharField(source='name', required=False)
    created = serializers.DateField(source='created', read_only=True)
    updated = serializers.DateField(source='updated', read_only=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'value', 'created', 'updated', 'active', )


class SponsorSerializer(serializers.ModelSerializer):
    logo = APIImageField(source='logo')

    class Meta:
        model = Sponsor
        fields = ('id', 'name', 'logo', 'website', 'active', 'order', )


class SocialMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialMedia
        fields = ('id', 'name', 'url', 'order', )

class QASerializer(serializers.ModelSerializer):

    class Meta:
        model = QA
        fields = ('id', 'question', 'answer', )

class CategorySerializer(serializers.ModelSerializer):
    qas = QASerializer(source='qa_set', many=True)

    class Meta:
        model = Category
        depth = 2
        fields = ('id', 'title', 'qas')


class TShirtSerializer(serializers.ModelSerializer):
    front_image = APIImageField(source='front_image')
    back_image = APIImageField(source='back_image')

    class Meta:
        model = TShirt
        fields = ('id', 'name', 'year', 'front_image', 'back_image', )


# TODO: move to machines app
from robocrm.models import Machine

class MachineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Machine
        fields = ('id', 'type', )
