from rest_framework import serializers
import sys
sys.path.append("....")
from core.models import User
sys.path.clear()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'fullname', 'phone_number', 'email','role','password']

        role = serializers.SerializerMethodField()

        def get_role(self,user):
            return user.role.role

