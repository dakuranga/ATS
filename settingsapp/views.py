from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from clients.models import Client
from signuplogin.models import User  
from .models import UserEmail
from .forms import UserEditForm, AttachmentForm
import urllib.parse
import re
from datetime import datetime, timedelta
from django.utils import timezone
import requests
from django.conf import settings
from requests_oauthlib import OAuth2Session
from django.conf import settings as django_settings



#Settings Home
@login_required
def settings(request):
    return render(request, 'settings.html')

#Settings Clients
@login_required
def settings_clients(request):
    client_list = Client.objects.all().order_by('name')      
    paginator = Paginator(client_list, 10) 
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)
    context = {'clients': clients}
    return render(request, 'settings_clients.html', context)

#Settings Users
from django.shortcuts import render
@login_required
def settings_users(request):
    current_team = request.user.team
    if current_team:
        users = User.objects.filter(team=current_team)
    else:
        users = User.objects.none()
    context = {'users': users}
    return render(request, 'settings_users.html', context)

@login_required
def settings_users_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings_users')  # Redirect to the user list or appropriate page
    else:
        form = UserEditForm(instance=user)
    return render(request, 'settings_users_edit.html', {'form': form, 'user_id': user_id})

@login_required
def settings_users_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_superuser:
        # Redirect or render an error page for normal users
        return HttpResponseForbidden("You don't have permission to access this page.")
    user.delete()
    return redirect('settings_users')

from .models import TenantUser
@login_required
def settings_email(request):
    try:
        tenant_user = TenantUser.objects.get(email=request.user.email)
    except TenantUser.DoesNotExist:
        emails = UserEmail.objects.none()  # Returns an empty queryset
    else:
        emails = UserEmail.objects.filter(user=tenant_user)

    return render(request, 'settings_email.html', {'emails': emails})

import logging
logger = logging.getLogger(__name__)

@login_required
def start_microsoft_auth(request):
    logger.debug(f"Starting Microsoft Auth - Current Tenant: {request.session.get('tenant')}")
    auth_base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": django_settings.MS_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": django_settings.MS_REDIRECT_URI,
        "scope": " ".join(django_settings.MS_SCOPES),
        "response_mode": "query",
    }
    
    auth_url = f"{auth_base_url}?{urllib.parse.urlencode(params)}"
    logger.debug(f"Redirecting to Microsoft Auth URL: {auth_url}")
    return HttpResponseRedirect(auth_url)

import logging

logger = logging.getLogger(__name__)

def handle_error(e):
    logger.error(f"Error: {e}")

@login_required
def microsoft_auth_callback(request):
    logger.debug(f"Microsoft Auth Callback - Current Tenant: {request.session.get('tenant')}")
    code = request.GET.get('code')
    if not code:
        logger.error("No code received in callback")
        return HttpResponse("Authentication failed.")
    

    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    token_data = {
        "client_id": django_settings.MS_CLIENT_ID,
        "scope": " ".join(django_settings.MS_SCOPES),
        "code": code,
        "redirect_uri": django_settings.MS_REDIRECT_URI,
        "grant_type": "authorization_code",
        "client_secret": django_settings.MS_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=token_data)
    token_response_data = response.json()
    logger.debug(f"Token Response Data: {token_response_data}")
    if 'access_token' in token_response_data:
        access_token = token_response_data['access_token']
        logger.debug(f"Access Token received: {access_token}")
        # Fetch the user's profile using the access token
        graph_url = "https://graph.microsoft.com/v1.0/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        profile_response = requests.get(graph_url, headers=headers)
        logger.debug(f"Profile Response Status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            email_address = profile_data.get("mail")  # Use the "mail" field to extract the email address
            logger.debug(f"Email Address from Profile: {email_address}")
        else:
            logger.error("Failed to fetch user profile.")
            return HttpResponse("Failed to fetch user profile.")
    else:
        logger.error("Failed to obtain access token.")
        return HttpResponse("Failed to obtain access token.")
    

    try:
        tenant_user = TenantUser.objects.get(email=request.user.email)
    except TenantUser.DoesNotExist:
        logger.debug(f"tenant user doesn not exist")
        # Handle the case where no corresponding TenantUser exists
        # This might include creating a TenantUser or returning an error
        return handle_error()

    # Now, use the tenant_user to create or update the UserEmail
    user_email = UserEmail(
        user=tenant_user,
        email_address=email_address,
        access_token=token_response_data.get("access_token"),
        refresh_token=token_response_data.get("refresh_token"),
        token_expiration=timezone.now() + timedelta(seconds=token_response_data.get("expires_in"))
    )
    user_email.save()
    
    logger.debug(f"UserEmail object created and saved for {request.user.email}")
    return redirect('settings_email')
  

def refresh_microsoft_token(user_email):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    
    data = {
        'client_id': django_settings.MS_CLIENT_ID,
        'client_secret': django_settings.MS_CLIENT_SECRET,
        'redirect_uri': django_settings.MS_REDIRECT_URI,
        'refresh_token': user_email.refresh_token,
        'grant_type': 'refresh_token'
    }
    
    response = requests.post(token_url, data=data)
    token_data = response.json()

    user_email.access_token = token_data['access_token']
    user_email.refresh_token = token_data['refresh_token']
    user_email.token_expiration = datetime.now() + timedelta(seconds=token_data['expires_in'])
    user_email.save()

def disconnect_email(request):
    try:
        user_email_obj = TenantUser.objects.get(email=request.user.email)
        user_email_obj.delete()
    except TenantUser.DoesNotExist:
        logger.debug(f"tenant user doesn not exist")
        # Handle the case where no corresponding TenantUser exists
        # This might include creating a TenantUser or returning an error
        return handle_error()
    
    return redirect('settings_email')


from .models import EmailSignature





@login_required
def settings_email(request):
    try:
        tenant_user = TenantUser.objects.get(email=request.user.email)
    except TenantUser.DoesNotExist:
        emails = UserEmail.objects.none()  # Returns an empty queryset
    else:
        emails = UserEmail.objects.filter(user=tenant_user)

    return render(request, 'settings_email.html', {'emails': emails})


@login_required
def settings_email_signature(request):
    try:
        tenant_user = TenantUser.objects.get(email=request.user.email)
        signatures = EmailSignature.objects.filter(user=tenant_user) 
    except TenantUser.DoesNotExist:
        signatures = [] 
    
    return render(request, 'settings_email_signature.html', {'signatures': signatures})

from .forms import EmailSignatureForm
@login_required
def create_email_signature(request):
    if request.method == 'POST':
        form = EmailSignatureForm(request.POST)
        if form.is_valid():
            email_signature = form.save(commit=False)
            try:
                tenant_user = TenantUser.objects.get(email=request.user.email)
            except TenantUser.DoesNotExist:
                pass

            if tenant_user:
                email_signature.user = tenant_user

             # Set the user field to the current user
            email_signature.save()
            return redirect('settings_email_signature')  # Redirect to a page displaying the list of email signatures
    else:
        form = EmailSignatureForm()
    
    return render(request, 'settings_email_signature_create.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from .models import EmailSignature
@login_required
def delete_signature(request, signature_id):
    signature = get_object_or_404(EmailSignature, id=signature_id)
    if request.method == 'POST':
        signature.delete()
    return redirect('email_signature_list')  # Assuming 'signature_list' is the name of your signature list view
@login_required
def edit_email_signature(request, signature_id):
    signature = get_object_or_404(EmailSignature, id=signature_id)
    if request.method == 'POST':
        form = EmailSignatureForm(request.POST, instance=signature)
        if form.is_valid():
            form.save()
            return redirect('email_signature_list')  # Redirect to the list of email signatures
    else:
        form = EmailSignatureForm(instance=signature)
    
    return render(request, 'create_email_signature.html', {'form': form, 'is_edit': True})






from django.shortcuts import render, redirect
from .models import EmailTemplate
from .forms import EmailTemplateForm
@login_required
def list_email_templates(request):
    templates = EmailTemplate.objects.all()
    return render(request, 'email_template_list.html', {'templates': templates})

from attachments.views import add_attachment
from settingsapp.models import TemplateAttachment

@login_required
def create_email_template(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save()
            attachments = request.FILES.getlist('attachments')

            for attachment in attachments:
                template_attachment = TemplateAttachment(template=template, file=attachment)
                template_attachment.save()

            return redirect('list_email_templates')
    else:
        form = EmailTemplateForm()
    return render(request, 'create_email_template.html', {'form': form})
@login_required
def edit_email_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('list_email_templates')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'create_email_template.html', {'form': form, 'is_edit': True})



from django.shortcuts import get_object_or_404, redirect
@login_required
def delete_email_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)
    template.delete()
    return redirect('list_email_templates')
