from django.conf import settings
from django.db import models, connection

from turnthepage.commons import generate_filename


class Category(models.Model):
    class Meta:
        verbose_name_plural = ''

    name = models.CharField(max_length=10)

    def __str__(self):
        return 'id:{} name:{}'.format(self.id, self.name)


class BookManger(models.Manager):
    def create_test_book(self, user):
        cursor = connection.cursor()
        params = ['title', 'author', 'publisher', 'category', 10000, 100, 'test.jpg', '2019-02-19', user.id]
        cursor.execute('INSERT INTO `books_book` (`title`, `author`, `publisher`, `category`, `price`, '
                       '`page_number`, `cover_url`, `target_date`, `user_id`) '
                       'VALUES (%s, %s, %s, %s ,%s ,%s, %s, %s, %s)', params)
        return Book.objects.last()


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    price = models.IntegerField()
    page_number = models.IntegerField()
    cover_url = models.ImageField(upload_to=generate_filename)
    target_date = models.DateField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = BookManger()

    def __str__(self):
        return 'id:{} user_id:{} title:{}'.format(self.id, self.user_id, self.title)


class Page(models.Model):
    comment = models.TextField()
    number = models.IntegerField()
    total_number = models.IntegerField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'id:{} book_id:{} user_id:{}'.format(self.id, self.book_id, self.user_id)
