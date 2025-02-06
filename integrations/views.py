from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Integration
from .serializers import IntegrationSerializer
from rest_framework.permissions import IsAuthenticated

class IntegrationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        integrations = Integration.objects.all()
        serializer = IntegrationSerializer(integrations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IntegrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IntegrationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            integration = Integration.objects.get(pk=pk)
        except Integration.DoesNotExist:
            return Response({"detail": "Integration not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = IntegrationSerializer(integration)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            integration = Integration.objects.get(pk=pk)
        except Integration.DoesNotExist:
            return Response({"detail": "Integration not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = IntegrationSerializer(integration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            integration = Integration.objects.get(pk=pk)
        except Integration.DoesNotExist:
            return Response({"detail": "Integration not found."}, status=status.HTTP_404_NOT_FOUND)

        integration.delete()
        return Response({"detail": "Integration deleted."}, status=status.HTTP_204_NO_CONTENT)
