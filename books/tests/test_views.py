from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from books.models import Book, Page
from conf.constants import USERNAME, PASSWORD
from conf.tests import BaseTestCase


class TestBookListView(BaseTestCase):
    def setUp(self):
        Book.objects.create_test_book(user=self.user)
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_book_list(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)

        book = response.context['book_list'][0]
        self.assertIsNone(book.page__number__sum)


class TestBookDetailView(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.book = Book.objects.create_test_book(user=cls.user)

    def setUp(self):
        Page.objects.create(total_number=50, number=50, comment='comment', book=self.book, user=self.user)
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_book_detail(self):
        response = self.client.get(reverse('books:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['book'])
        self.assertIsNotNone(response.context['pages'])


class TestBookCreateView(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {'title': 'title', 'author': 'author', 'publisher': 'publisher', 'category': 'category',
                    'price': 10000, 'page_number': 100, 'target_date': '2019-02-19'}
        cls.path = reverse('books:book_create')

    def setUp(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_create_book(self):
        # client post에 file을 어떻게 전달하지
        data = self.data.copy()
        data['cover_url'] = SimpleUploadedFile('title.png', None, content_type='image/png')
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form(self):
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, 200)


class TestPageCreateView(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.book = Book.objects.create_test_book(user=cls.user)
        cls.path = reverse('books:page_create', args=[cls.book.id])

    def setUp(self):
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_create_page(self):
        data = {'total_number': 50, 'comment': 'comment'}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Page.objects.count(), 1)

    def test_invalid_form(self):
        data = {'total_number': 1000, 'comment': 'comment'}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 400)

        data = {'total_number': 10, 'comment': ''}
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, 400)
