from datetime import timedelta

from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from accounts.models import Token
from turnthepage.commons import get_random_string
from turnthepage.decorators import already_logged_in
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

        token = get_random_string(20)
        expiry_date = datetime.now() + timedelta(hours=1)
        Token.objects.create(name=token, expiry_date=expiry_date, user=user)

        subject = '[turnthepage] 이메일 인증요청입니다.'
        from_email = 'admin@gureuso.me'

        uri = '{0}?token={1}&email={2}'.format(request.build_absolute_uri(), token, user.email)
        html_message = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        .jumbotron {{
            padding: 2rem 1rem;
            margin-bottom: 2rem;
            background-color: #e9ecef;
            border-radius: .3rem;
        }}
        </style>
        </head>
        <body>
        <div class="jumbotron">
          <h1 class="display-4">이메일 인증요청입니다.</h1>
          <hr class="my-4">
          <p>{0}님 turnthepage 이메일 인증요청입니다. 아래 버튼을 클릭해서 인증해주세요:)</p>
          <a class="btn btn-primary btn-lg" href="{1}" role="button">인증하기</a>
        </div>
        </body>
        </html>
        """.format(user.username, uri)

        send_mail(subject=subject, message=None, from_email=from_email, recipient_list=[user.email],
                  html_message=html_message)
        return HttpResponse()
