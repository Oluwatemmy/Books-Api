from rest_framework.test import APITestCase
from rest_framework import status
from books.models import Book
from django.urls import reverse

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            language="English",
        )
        self.valid_payload = {
            "title": "New Book",
            "author": "Jane Doe",
            "language": "Spanish",
        }
        self.invalid_payload = {
            "title": "",  # Invalid because title is required
            "author": "No Name",
            "language": "French",
        }

    def test_create_book(self):
        url = reverse('book-create')
        response = self.client.post(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.valid_payload['title'])

    def test_create_book_with_invalid_data(self):
        url = reverse('book-create')
        response = self.client.post(url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_list_all_books(self):
        url = reverse('book-list-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_retrieve_nonexistent_book(self):
        url = reverse('book-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_nonexistent_book(self):
        url = reverse('book-delete', args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
