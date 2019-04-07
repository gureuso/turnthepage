from books.forms import PageCreateForm
from books.models import Book, Page
from turnthepage.tests import BaseTestCase


class PageCreateFormTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.comment = 'comment'
        cls.book = None

    def setUp(self):
        self.book = Book.objects.create_test_book(user=self.user)

    def test_minus_total_number(self):
        data = {'total_number': -1, 'comment': self.comment, 'book_id': self.book.id}
        form = PageCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_over_total_number(self):
        data = {'total_number': 101, 'comment': self.comment, 'book_id': self.book.id}
        form = PageCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_total_number(self):
        Page.objects.create(comment=self.comment, total_number=80, number=80, book=self.book, user=self.user)

        data = {'total_number': 60, 'comment': self.comment, 'book_id': self.book.id}
        form = PageCreateForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'total_number': 80, 'comment': self.comment, 'book_id': self.book.id}
        form = PageCreateForm(data=data)
        self.assertFalse(form.is_valid())
