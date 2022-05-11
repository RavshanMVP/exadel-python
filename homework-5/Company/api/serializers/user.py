from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.user import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'phone_number', 'email','role_id']

