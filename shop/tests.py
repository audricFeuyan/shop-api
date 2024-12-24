from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category

class TestCategory(APITestCase):
    url = reverse_lazy('category-list')

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def test_list(self):
        category = Category.objects.create(name='Fruit', active=True)
        Category.objects.create(name='Légumes', active=False)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id': category.pk,
                'name': category.name,
            }
        ]

        self.assertEqual(expected, response.json())


    def test_create(self):
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})

        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.exists())