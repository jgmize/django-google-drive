import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseRedirect)

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
import httplib2

from .models import DriveCredential


ALL_SCOPES = ('https://www.googleapis.com/auth/drive.install '
              'https://www.googleapis.com/auth/drive.file '
              'https://www.googleapis.com/auth/userinfo.email '
              'https://www.googleapis.com/auth/userinfo.profile')


@login_required  # TODO: login via google
def add_account(request):
    flow = flow_from_clientsecrets(
        settings.GDRIVE_CLIENT_SECRETS, scope=ALL_SCOPES)
    flow.redirect_uri = getattr(
        settings, 'GDRIVE_OAUTH2_CALLBACK_URI', 'http://%s%s' % (
        Site.objects.get_current().domain,
        reverse('gdoauth2_callback')))
    request.session['gdrive_flow'] = flow
    request.session.save()
    return HttpResponseRedirect(flow.step1_get_authorize_url())


@login_required
def callback(request):
    flow = request.session.get('gdrive_flow')
    if not flow:  # TODO: handle this better
        return HttpResponseForbidden('no flow for you')
    dc = DriveCredential()
    dc.credential = flow.step2_exchange(request.REQUEST)
    user_info_service = build(
        serviceName='oauth2', version='v2',
        http=dc.credential.authorize(httplib2.Http()))
    try:
        dc.user_info = user_info_service.userinfo().get().execute()
    except Exception, e:
        logging.error('An error occurred: %s', e)
    del request.session['gdrive_flow']
    dc.save()
    return HttpResponse('added credential for %s' % dc.user_info)
