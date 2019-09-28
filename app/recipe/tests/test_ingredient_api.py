from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientTests(TestCase):
    """Tests the publicly available Ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Tests that you need to be logged in to see ingredients"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPI(TestCase):
    """Tests the logged in Ingredient API endpoint"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retreive_ingredient_list(self):
        """Tests that we can retreive ingredients."""
        Ingredient.objects.create(user=self.user, name='Pilpel')
        Ingredient.objects.create(user=self.user, name='Bamba')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_ingidients_limited_by_user(self):
        """Tests that only ONgreidnet owned by User are presented"""
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'passwrod123'
        )
        ingredient = Ingredient.objects.create(user=self.user, name='Pilpel')
        Ingredient.objects.create(user=user2, name='Bamba')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test success creation of ingredient"""
        payload = {'name': 'Salt'}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ingredient = Ingredient.objects.filter(user=self.user,
                                               name=payload['name'])
        self.assertTrue(ingredient.exists())

    def test_create_ingredient_invalid(self):
        """Tests create invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
