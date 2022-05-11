from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

import sys
sys.path.append("...")
from api.serializers.role import RoleSerializer, Role

@api_view (['GET'])
def RoleList(request):
    if request.method == "GET":
        roles  = Role.objects.all()
        serializer = RoleSerializer(roles,many= True)
        return Response(serializer.data )


class RoleDetails(GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)





