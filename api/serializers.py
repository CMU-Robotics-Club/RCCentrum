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
from posters.models import Poster
from .fields import ProjectActiveField
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from django.contrib.contenttypes.models import ContentType

class WebcamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webcam
        fields = ('id', 'name', 'url', )


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for key, value in ret.items():
            method = getattr(self, 'transform_' + key, None)
            if method is not None:
                ret[key] = method(value)
        return ret

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active',)


class RoboUserSerializer(serializers.ModelSerializer):
    
    magnetic = serializers.BooleanField(source='is_magnetic_set')
    rfid = serializers.BooleanField(source='is_rfid_set')

    # TODO: find better way to do this
    def to_representation(self, obj):
        """
        Hack to embed 'user' fields into main object
        eliminating nested fields.
        """

        if obj is None:
            return {}

        ret = super().to_representation(obj)
        p_serializer = UserSerializer(obj.user, context=self.context)
        p_ret = p_serializer.to_representation(obj.user)

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
        fields = ('id', 'magnetic', 'rfid', 'machines', )


class ProjectSerializer(serializers.ModelSerializer):
    active = ProjectActiveField(source='last_api_activity')

    class Meta:
        model = Project
        fields = ('id', 'name', 'image', 'blurb', 'description', 'website', 'display', 'leaders', 'active', 'last_api_activity', )


class OfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = ('id', 'position', 'user', 'image', 'description', 'order', )


class ChannelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    created = serializers.DateTimeField(source='created_datetime', read_only=True)
    updated = serializers.DateTimeField(source='updated_datetime', read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['updater_type_id'] = ContentType.objects.get_for_model(user).id
        validated_data['updater_id'] = user.id

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.updater_object = user
        return super().update(instance, validated_data)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'value', 'created', 'updated', 'active', 'description', )


class SponsorSerializer(serializers.ModelSerializer):

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
    class Meta:
        model = TShirt
        fields = ('id', 'name', 'year', 'front_image', 'back_image', )


class PosterSerializer(serializers.ModelSerializer):

    image_thumb = serializers.SerializerMethodField('image_thumb_url')

    class Meta:
        model = Poster
        fields = ('id', 'name', 'year', 'image_thumb', 'image', )

    def image_thumb_url(self, obj):
        url = thumbnail_url(obj.image, 'poster_index')
        return self.context['request'].build_absolute_uri(url)


# TODO: move to machines app
from robocrm.models import Machine

class MachineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Machine
        fields = ('id', 'type', )
