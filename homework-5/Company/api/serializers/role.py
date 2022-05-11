from rest_framework import serializers
import sys
sys.path.append("....")
from core.models.role import Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']

