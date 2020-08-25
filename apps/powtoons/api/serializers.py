from rest_framework import serializers

from django.contrib.auth.models import User
from apps.powtoons.models import Powtoon


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username']

class PowtoonGetSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    shared_with = UserSerializer(many=True)

    class Meta:
        model = Powtoon
        fields = [
            'id', 'name', 'owner', 'shared_with'
        ]
        read_only_fields = fields

class PowtoonCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Powtoon
        fields = [
            'id', 'name', 'owner', 'shared_with'
        ]
        optional_fields = ['shared_with', ]
