from rest_framework import serializers

from core.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id', 'fullname', 'phone_number', 'email','role']

    role = serializers.SerializerMethodField()

    def get_role(self,user):
        return user.role.role

