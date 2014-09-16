from rest_framework import serializers
from django.contrib.auth.models import User
from robocrm.models import RoboUser
from projects.models import Project
from officers.models import Officer

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

        fields = ('id', 'club_rank', )

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'image', 'blurb', 'description', 'website', 'display', 'leaders', 'last_api_activity', )

class OfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = ('id', 'position', 'user', 'image', 'description', )
