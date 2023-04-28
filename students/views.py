import jwt
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import (
    views,
    generics,
    status,
    permissions
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from .models import (
    Flow, 
    Direction, 
    Student,
    User
)
from .serializers import (
    FlowSerializer,
    DirectionSerializer,
    StudentSerializer,
    UserSerializer,
    RegistrationSerializer,
    AuthSerializer, 
)



class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny ,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        user_payload = {
            'user_id': user.id,
            'username': user.username
        }
        tokens = {
            'access_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256"),
            'refresh_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256")
        }

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'tokens': tokens
        }
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

        
class AuthView(generics.GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerializer
    permission_classes = [permissions.IsAdminUser,]


class FlowListAPIView(generics.ListAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer


class FlowCreateAPIView(generics.CreateAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer


class DirectionListAPIView(generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class DirectionCreateAPIView(generics.CreateAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDestroyAPIView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer