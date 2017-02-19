from django.views import View
from django.template.response import TemplateResponse
from mailtrail.utils import get_template


class EmailResendView(View):
    def get(self, request, pk):
        return TemplateResponse(request, template=get_template('email', 'resend.html'))
