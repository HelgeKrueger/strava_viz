from rest_framework import serializers
from django_enum_choices.serializers import EnumChoiceModelSerializerMixin

from .models import StravaActivity


class StravaActivitySerializer(EnumChoiceModelSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StravaActivity
        fields = ['datetime', 'distance_meter', 'activity_type']
