from django.conf import settings
from django.db import models, connection

from conf.commons import generate_filename


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=10)

    def __str__(self):
        return 'id:{} name:{}'.format(self.id, self.name)


class BookManger(models.Manager):
    def create_test_book(self, user, target_date='2099-02-19'):
        category = Category.objects.filter(name='IT').first() or Category.objects.create(name='IT')
        cursor = connection.cursor()
        params = ['title', 'author', 'publisher', category.id, 10000, 100, 'test.jpg', target_date, user.id]
        cursor.execute('INSERT INTO `books_book` (`title`, `author`, `publisher`, `category_id`, `price`, '
                       '`page_number`, `cover_url`, `target_date`, `user_id`) '
                       'VALUES (%s, %s, %s, %s ,%s ,%s, %s, %s, %s)', params)
        cursor.close()
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

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


class AdminCoupon(models.Model):
    name = models.CharField(max_length=20)
    text = models.CharField(max_length=100, null=True)
    coupon_url = models.ImageField(upload_to=generate_filename)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'id:{} name:{}'.format(self.id, self.name)


class CouponManger(models.Manager):
    def create_coupon(self, form, book, user):
        if book.page_number != form.cleaned_data['total_number']:
            return
        admin_coupon = AdminCoupon.objects.last()
        Coupon.objects.create(admin_coupon=admin_coupon, user=user, book=book)


class Coupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admin_coupon = models.ForeignKey(AdminCoupon, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    objects = CouponManger()

    def __str__(self):
        return 'id:{} book_id:{} name:{}'.format(self.id, self.book_id, self.admin_coupon.name)
