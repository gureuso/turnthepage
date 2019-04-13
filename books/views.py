from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Page, Category
from .forms import PageCreateForm


class BookListView(LoginRequiredMixin, ListView):
    queryset = Book.objects.annotate(Sum('page__number'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    queryset = Book.objects.annotate(Sum('page__number'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = Page.objects.filter(book_id=self.kwargs['pk']).order_by('-id')
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'publisher', 'price', 'page_number', 'cover_url', 'target_date', 'category']
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
        Page.objects.create(number=number, total_number=total_number, comment=comment, user=request.user, book=book)
        return HttpResponse()
