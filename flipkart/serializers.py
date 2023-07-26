from rest_framework import serializers
from .models import Registration


class ecomserializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
