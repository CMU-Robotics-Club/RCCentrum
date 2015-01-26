from rest_framework import serializers
from .models import APIRequest
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
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from django.contrib.contenttypes.models import ContentType

class BalanceSerializer(serializers.Serializer):
    """
    To validate /users/:id/balance/ endpoint.
    """

    amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    meta = serializers.CharField(required=False, allow_blank=True)


class EmailSerializer(serializers.Serializer):
    """
    To validate /users/:id/email/ endpoint.
    """
    
    subject = serializers.CharField()
    content = serializers.CharField()
    meta = serializers.CharField(required=False, allow_blank=True)


class RFIDSerializer(serializers.Serializer):
    """
    To validate /rfid/ and /users/:id/rfid/ lookup endpoint.
    """

    rfid = serializers.CharField()
    meta = serializers.CharField(required=False, allow_blank=True)

    def validate_rfid(self, value):
        """
        Ensures the RFID is the proper length
        """

        if len(value) != 8:
            raise serializers.ValidationError("RFIDs must be 8 characters long")

        return value


class MagneticSerializer(serializers.Serializer):
    """
    To validate /magnetic/ lookup endpoint.
    """

    magnetic = serializers.CharField()
    meta = serializers.CharField(required=False, allow_blank=True)

    def validate_magnetic(self, value):
        """
        Ensures the Magnetic ID is the proper length
        """

        if len(value) != 9:
            raise serializers.ValidationError("Magnetic IDs must be 9 characters long")

        return value


class APIRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = APIRequest
        fields = ('id', 'endpoint', 'extra', 'user', 'updater_is_project', 'updater_id', 'created_datetime', 'updated_datetime', 'success', 'meta', )


class WebcamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Webcam
        fields = ('id', 'name', 'url', )


class RoboUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)

    magnetic = serializers.BooleanField(source='is_magnetic_set', read_only=True)
    rfid = serializers.BooleanField(source='is_rfid_set', read_only=True)
    machines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = RoboUser
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'magnetic', 'rfid', 'balance', 'machines', )


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'image', 'blurb', 'description', 'website', 'display', 'leaders', 'last_api_activity', )


class OfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = ('id', 'position', 'user', 'image', 'description', 'order', )


class ChannelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(source='created_datetime', read_only=True)
    updated = serializers.DateTimeField(source='updated_datetime', read_only=True)
    description = serializers.CharField(read_only=True)

    # TODO: bring this functionality to all ModelSerializers
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(kwargs, 'context'):
            request = kwargs['context']['request']
            params = request.QUERY_PARAMS
            fields = params.get('fields')
            exclude = params.get('exclude')

            if fields is not None:
                if "," in fields:
                    fields = fields.split(',')
                else:
                    fields = [fields]

                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    if field_name in self.fields:
                        self.fields.pop(field_name)

            if exclude is not None:
                if "," in exclude:
                    exclude = exclude.split(',')
                else:
                    exclude = [exclude]

                disallowed = set(exclude)
                existing = set(self.fields.keys())
                for field_name in disallowed:
                    if field_name in self.fields:
                        self.fields.pop(field_name)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.updater_object = user
        return super().update(instance, validated_data)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'value', 'created', 'updated', 'description', )


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
