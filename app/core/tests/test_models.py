from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='testpass'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """Test creating a new user with an email is succesful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests that the email was normalized to lower case"""
        email = 'test@SOMEDOMAIN.Com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Tests that the invalid email rases the proper fault error"""
        # the code below expects to get a ValueError
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_createsupperuser(self):
        """Tests that when a superuser is crated the is_staff is valid. """
        user = get_user_model().objects.create_superuser(
            'test@someweb.org',
            'test123'
            )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Tests Ingredient creation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cuecamber'
            )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Tests Recipe creation and string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='STake and mashroom souce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
