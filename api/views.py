from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .models import Restaurant, Menu, Vote
from .serializers import (
    CreateEmployeeSerializer,
    CreateRestaurantAdminSerializer,
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializer
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import date

class CreateEmployeeView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class CreateRestaurantAdminView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateRestaurantAdminSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

class IsRestaurantAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsRestaurantAdmin]

    def perform_create(self, serializer):
        restaurant = self.request.user.restaurants.first()
        serializer.save(restaurant=restaurant)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        menu = self.get_object()
        user = request.user
        vote, created = Vote.objects.get_or_create(user=user, menu=menu, date=date.today())
        if created:
            menu.total_votes += 1
            menu.save()
            return Response({'status': 'vote added'})
        else:
            return Response({'status': 'already voted'}, status=400)

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

class TodayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.filter(date=date.today())

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        vote_results = {menu['id']: menu['total_votes'] for menu in serializer.data}
        return Response({'menus': serializer.data, 'vote_results': vote_results})
