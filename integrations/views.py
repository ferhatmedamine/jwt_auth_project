from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Integration, MoodleIntegration
from .serializers import IntegrationSerializer, MoodleIntegrationSerializer
from rest_framework.permissions import IsAuthenticated
from .helpers import get_moodle_courses, get_moodle_grades  


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

        serializer = IntegrationSerializer(integration, data=request.data, partial=True)
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

# New Moodle Integration Views
class MoodleIntegrationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        moodle_integrations = MoodleIntegration.objects.all()
        serializer = MoodleIntegrationSerializer(moodle_integrations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodleIntegrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoodleIntegrationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            moodle_integration = MoodleIntegration.objects.get(pk=pk)
        except MoodleIntegration.DoesNotExist:
            return Response({"detail": "Moodle Integration not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch courses and grades from Moodle API
        courses = get_moodle_courses(moodle_integration.moodle_url, moodle_integration.api_key)
        grades = []
        if courses:
            for course in courses:
                course_id = course.get('id')
                course_grades = get_moodle_grades(moodle_integration.moodle_url, moodle_integration.api_key, course_id)
                grades.append(course_grades)

        # Update the MoodleIntegration instance with the fetched courses and grades
        moodle_integration.courses = courses
        moodle_integration.grades = grades
        moodle_integration.save()

        # Serialize and return the updated integration data with courses and grades
        serializer = MoodleIntegrationSerializer(moodle_integration)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            moodle_integration = MoodleIntegration.objects.get(pk=pk)
        except MoodleIntegration.DoesNotExist:
            return Response({"detail": "Moodle Integration not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MoodleIntegrationSerializer(moodle_integration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            moodle_integration = MoodleIntegration.objects.get(pk=pk)
        except MoodleIntegration.DoesNotExist:
            return Response({"detail": "Moodle Integration not found."}, status=status.HTTP_404_NOT_FOUND)

        moodle_integration.delete()
        return Response({"detail": "Moodle Integration deleted."}, status=status.HTTP_204_NO_CONTENT)