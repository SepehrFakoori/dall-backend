from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateUploadSerializer
from . import services


class CreateUploadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = services.create_upload(
            user=request.user,
            **serializer.validated_data,
        )
        return Response(result, status=status.HTTP_201_CREATED)
