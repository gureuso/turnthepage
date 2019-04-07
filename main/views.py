from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class FaviconView(RedirectView):
    url = '/static/favicon.ico'
    permanent = True


class IndexView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('books:book_list')
