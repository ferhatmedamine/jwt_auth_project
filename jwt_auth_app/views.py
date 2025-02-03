from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer


# Get the custom User model
User = get_user_model()


# RegisterView for user registration
class RegisterView(APIView):
    
    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            user.set_password(request.data['password'])
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LoginView for user login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)  # Authenticate the user

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)  # Get or create the token
        serializer = UserSerializer(user)

        return Response({'token': token.key, 'user': serializer.data})


# LogoutView for user logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # Delete the token to log out
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except (AttributeError, TypeError):
            return Response({"detail": "No active session."}, status=status.HTTP_400_BAD_REQUEST)
