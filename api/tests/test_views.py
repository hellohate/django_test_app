from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Restaurant, Menu  # Update import path for models

class APITest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', email='admin@example.com', is_staff=True)
        self.employee_user = User.objects.create_user(username='employee', password='employeepassword', email='employee@example.com')

    def test_create_restaurant_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('create_restaurant_admin')
        data = {'username': 'restadmin', 'password': 'restpassword', 'email': 'restadmin@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_employee(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('create_employee')
        data = {'username': 'newemployee', 'password': 'newpassword', 'email': 'newemployee@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_restaurant(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('restaurant-list')
        data = {'name': 'Test Restaurant'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_create_menu_and_vote(self):
        self.client.force_authenticate(user=self.admin_user)
        restaurant = Restaurant.objects.create(name='Test Restaurant', owner=self.admin_user)
        url = reverse('menu-list')
        data = {'name': 'Today Menu', 'description': 'Description of today menu', 'restaurant': restaurant.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)

        menu_id = response.data['id']

        self.client.force_authenticate(user=self.employee_user)
        url = reverse('menu-vote', kwargs={'pk': menu_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'vote added')

    def test_get_today_menu_with_votes(self):
        self.client.force_authenticate(user=self.admin_user)
        restaurant = Restaurant.objects.create(name='Test Restaurant', owner=self.admin_user)
        menu = Menu.objects.create(name='Today Menu', description='Description of today menu', restaurant=restaurant)
        url = reverse('today_menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['menus']), 1)
        self.assertEqual(response.data['menus'][0]['total_votes'], 1)
