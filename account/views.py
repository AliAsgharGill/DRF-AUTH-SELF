from django.shortcuts import render
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Token generation for the user
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = (UserRenderer, )
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Remove 'password2' from the serialized data before returning
        user_data = serializer.data.copy()
        user_data.pop('password2', None)  # Safely remove the 'password2' field

        token = get_token_for_user(user)

        # Send the filtered user data and token in the response
        return Response({'user': user_data, 'token': token}, status=status.HTTP_201_CREATED)