from rest_framework import serializers
from .models import TGUser

class TGUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TGUser
        fields = ["id", "user_id", "username", "created_at"]

