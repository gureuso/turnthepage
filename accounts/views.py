from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from turnthepage.decorators import already_logged_in
from .forms import SignupForm


class SignupView(FormView):
    template_name = 'registration/signup.html'
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
