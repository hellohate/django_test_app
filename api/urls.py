from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantViewSet,
    MenuViewSet,
    VoteViewSet,
    CreateEmployeeView,
    CreateRestaurantAdminView,
    TodayMenuView
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-employee/', CreateEmployeeView.as_view(), name='create_employee'),
    path('create-restaurant-admin/', CreateRestaurantAdminView.as_view(), name='create_restaurant_admin'),
    path('today-menu/', TodayMenuView.as_view(), name='today_menu'),
]
