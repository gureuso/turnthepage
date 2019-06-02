from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from conf.emails import WinAPrizeEmail
from .models import Book, Page, Category, Coupon
from .forms import PageCreateForm, BookRenewForm, BookCreateForm


class BookListView(LoginRequiredMixin, ListView):
    queryset = Book.objects.annotate(Sum('page__number'))


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    queryset = Book.objects.annotate(Sum('page__number'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = Page.objects.filter(book_id=self.kwargs['pk']).order_by('-id')
        return context


class BookCreateView(LoginRequiredMixin, FormView):
    form_class = BookCreateForm
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        data = form.cleaned_data
        Book.objects.create(title=data['title'], author=data['author'], publisher=data['publisher'], price=data['price'],
                            page_number=data['page_number'], cover_url=data['cover_url'], target_date=data['target_date'],
                            category=data['category'], user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BookRenewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        data = request.POST.copy()
        data['book_id'] = pk

        form = BookRenewForm(data)
        if not form.is_valid():
            return HttpResponse(status=400)

        target_date = form.cleaned_data['target_date']
        Book.objects.filter(pk=pk).update(target_date=target_date)
        return HttpResponse()


class PageCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        data = request.POST.copy()
        data['book_id'] = pk

        form = PageCreateForm(data)
        if not form.is_valid():
            return HttpResponse(status=400)

        book = form.cleaned_data['book']
        comment = form.cleaned_data['comment']
        number = form.cleaned_data['number']
        total_number = form.cleaned_data['total_number']

        WinAPrizeEmail(request=request, form=form, user=request.user, book=book).send_mail()
        Coupon.objects.create_coupon(form=form, book=book, user=request.user)
        Page.objects.create(number=number, total_number=total_number, comment=comment, user=request.user, book=book)
        return HttpResponse()
