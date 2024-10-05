from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Breed, Kitten, Rating
from .serializers import BreedSerializer, KittenSerializer, RatingSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # Получение списка пород
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Получение подробной информации о породе (если необходимо)
        return super().retrieve(request, *args, **kwargs)

class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['breed']
    search_fields = ['breed__name', 'color', 'description']

    def list(self, request, *args, **kwargs):
        # Получение списка всех котят (с возможностью фильтрации по породе)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Получение подробной информации о котенке
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Добавление информации о котенке
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Устанавливаем владельца котенка
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        # Изменение информации о котенке
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Частичное изменение информации о котенке
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Удаление информации о котенке
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rate(self, request, pk=None):
        kitten = self.get_object()
        data = request.data.copy()
        data['kitten'] = kitten.id  # Добавляем поле 'kitten' в данные

        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]