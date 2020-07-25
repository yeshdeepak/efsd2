from io import BytesIO
from io import StringIO  ## for Python 3
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .models import *
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from efs import settings
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from xhtml2pdf import pisa
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.core.mail import EmailMessage
from django.template.loader import get_template
from io import BytesIO
from efs import settings


def render_to_pdf(user_email,template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    # PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    #send_mail('Example Subject', 'Example message', 'yesh080690@gmail.com', ['jdyesh@gmail.com'])
    mail = EmailMessage("Portfolio", "", 'yesh080690@gmail.com', [user_email])

    mail.attach("Your Portfolio", result.getvalue(), 'application/pdf')
    mail.send()
    if not pdf.err:

        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
