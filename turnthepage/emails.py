from django.core.mail import send_mail

from turnthepage.constants import DEFAULT_FROM_EMAIL


def get_html_message(body):
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
    {0}
    </body>
    </html>
    """.format(body)
    return html_message


class VerifyEmail:
    def __init__(self, request, token, user):
        self.request = request
        self.token = token
        self.user = user
        self.uri = self.get_uri()

    def get_uri(self):
        return '{0}?token={1}&email={2}'.format(self.request.build_absolute_uri(), self.token.name, self.user.email)

    def get_html_message(self):
        body = """
        <div class="jumbotron">
          <h1 class="display-4">이메일 인증요청입니다.</h1>
          <hr class="my-4">
          <p>{0}님 turnthepage 이메일 인증요청입니다. 아래 버튼을 클릭해서 인증해주세요:)</p>
          <a class="btn btn-primary btn-lg" href="{1}" role="button">인증하기</a>
        </div>
        """.format(self.user.username, self.uri)
        return get_html_message(body)

    def send_email(self):
        subject = '[turnthepage] 이메일 인증요청입니다.'
        html_message = self.get_html_message()
        send_mail(subject=subject, message=None, from_email=DEFAULT_FROM_EMAIL, recipient_list=[self.user.email],
                  html_message=html_message)


class WinAPrizeEmail:
    def __init__(self, request, form, user, book):
        self.request = request
        self.form = form
        self.user = user
        self.book = book

    def get_html_message(self):
        body = """
        <div class="jumbotron">
          <h1 class="display-4">미션 성공 알람입니다.</h1>
          <hr class="my-4">
          <p>{0}님 turnthepage 미션을 성공했습니다. 축하드립니다. 아래 QR코드를 촬영하면 스타벅스 무료 쿠폰이 발급됩니다.</p>
          <img src="{1}/static/images/QR.png">
        </div>
        """.format(self.user.username, self.request.META['HTTP_HOST'])
        return get_html_message(body)

    def send_mail(self):
        if self.book.page_number != self.form.cleaned_data['total_number']:
            return

        subject = '[turnthepage] 미션 성공 알람입니다.'
        html_message = self.get_html_message()
        send_mail(subject=subject, message=None, from_email=DEFAULT_FROM_EMAIL, recipient_list=[self.user.email],
                  html_message=html_message)
