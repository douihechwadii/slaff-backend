from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.hashers import make_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
class RegisterFirstUserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        if User.objects.exists():
            return Response({'error': 'Admin already created.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        data['is_staff'] = True
        data['is_superuser'] = True
        data['password'] = make_password(data['password'])
        
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Admin registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)