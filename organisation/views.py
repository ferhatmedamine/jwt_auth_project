from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.permissions import IsAuthenticated

class OrganisationListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response({"detail": "Organisation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            organisation = Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            return Response({"detail": "Organisation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganisationSerializer(organisation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            organisation = Organisation.objects.get(pk=pk)
            organisation.delete()
            return Response({"detail": "Organisation deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Organisation.DoesNotExist:
            return Response({"detail": "Organisation not found."}, status=status.HTTP_404_NOT_FOUND)
