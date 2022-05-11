from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

import sys
sys.path.append("...")
from api.serializers.request_status import RequestStatusSerializer, RequestStatus

@api_view (['GET'])
def RequestStatusList(request):
    if request.method == "GET":
        statuses  = RequestStatus.objects.all()
        serializer = RequestStatusSerializer(statuses,many= True)
        return Response(serializer.data )


class RequestStatusDetails(GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = RequestStatusSerializer
    queryset = RequestStatus.objects.all()

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
