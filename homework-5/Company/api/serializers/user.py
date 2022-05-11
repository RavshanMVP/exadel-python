from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.user import User
sys.path.clear()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'fullname', 'phone_number', 'email','role_id']

        role_id = serializers.SerializerMethodField()

        def get_role(self,user):
            return user.role_id.role

