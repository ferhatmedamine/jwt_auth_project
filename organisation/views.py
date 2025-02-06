from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()  # Access User model

class OrganisationListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        try:
            organisations = Organisation.objects.all()
            serializer = OrganisationSerializer(organisations, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"Error fetching organisations: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = OrganisationSerializer(data=request.data)
            if serializer.is_valid():
                # Automatically associate the logged-in user with the organisation
                serializer.save(user=request.user)  
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error creating organisation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request, pk):
        try:
            organisation = Organisation.objects.get(pk=pk)
            serializer = OrganisationSerializer(organisation)
            return Response(serializer.data)
        except Organisation.DoesNotExist:
            return Response({"detail": "Organisation not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Error fetching organisation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            organisation = Organisation.objects.get(pk=pk)
            if organisation.user != request.user:  # Ensure the logged-in user is the owner
                return Response({"detail": "You do not have permission to edit this organisation."}, status=status.HTTP_403_FORBIDDEN)

            serializer = OrganisationSerializer(organisation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Organisation.DoesNotExist:
            return Response({"detail": "Organisation not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Error updating organisation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            organisation = Organisation.objects.get(pk=pk)
            if organisation.user != request.user:  # Ensure the logged-in user is the owner
                return Response({"detail": "You do not have permission to delete this organisation."}, status=status.HTTP_403_FORBIDDEN)

            organisation.delete()
            return Response({"detail": "Organisation deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Organisation.DoesNotExist:
            return Response({"detail": "Organisation not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Error deleting organisation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
