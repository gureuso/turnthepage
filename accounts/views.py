from datetime import timedelta

from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from accounts.models import Token
from books.models import Book, AdminCoupon
from turnthepage.commons import get_random_string
from turnthepage.decorators import already_logged_in
from turnthepage.emails import VerifyEmail
from .forms import SignupForm, VerifyEmailForm


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = settings.LOGIN_REDIRECT_URL

    @method_decorator(already_logged_in)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        UserModel = get_user_model()
        user = UserModel.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(self.request, user)
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_all_cnt'] = Book.objects.count()
        context['book_success_cnt'] = Book.objects.filter(page_number=F('page__total_number')).count()
        context['book_fail_cnt'] = Book.objects.filter(target_date__lt=datetime.utcnow().strftime('%Y-%m-%d')).count()
        context['coupons'] = AdminCoupon.objects.filter(coupon__user_id=self.request.user.id,
                                                        id=F('coupon__admin_coupon_id'))
        return context


class VerifyEmailView(LoginRequiredMixin, View):
    def get(self, request):
        form = VerifyEmailForm(request.GET)
        if not form.is_valid():
            raise SuspiciousOperation()

        request.user.verified_email = True
        request.user.save()

        return redirect(reverse('accounts:profile'))

    def post(self, request):
        user = request.user
        if user.verified_email:
            return HttpResponse(status=400)

        token_name = get_random_string(20)
        expiry_date = datetime.now() + timedelta(hours=1)
        token = Token.objects.create(name=token_name, expiry_date=expiry_date, user=user)
        VerifyEmail(request=request, token=token, user=user).send_email()
        return HttpResponse()
