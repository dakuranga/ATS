# inout/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            User.objects.send_confirmation_email(user, request)
            request.session['user_email_for_activation'] = user.email
            return redirect('account_activation_sent')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.shortcuts import resolve_url

def redirect_if_authenticated(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with the name of your home page view
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@redirect_if_authenticated
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        from .backends import AllowInactiveUserModelBackend
        backend = AllowInactiveUserModelBackend()
        user = backend.authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_verified:
                login(request, user)
                
                domain = user.email.split('@')[-1]
                db_alias = f'team_{domain.replace(".", "_")}'
                request.session['db_alias'] = db_alias  # Store database alias in session

                request.session.save()
                return redirect(resolve_url('home'))
            else:
                messages.error(
                    request,
                    'Your account is not verified. Please verify your email address.'
                )
                return render(request, 'login.html')

        messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import User


def confirm_email(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'email_confirmation_invalid.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'email_confirmation_invalid.html')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def resend_activation(request):
    user_email = request.session.get(
        'user_email_for_activation')  # Get email from session
    if user_email:
        user = User.objects.filter(email=user_email).first()
        if user:
            User.objects.send_confirmation_email(user, request)
            messages.success(
                request,
                'A new activation email has been sent to your email address.')
        else:
            messages.error(
                request, 'There was a problem resending the activation email.')
    else:
        messages.error(request,
                       'There was a problem resending the activation email.')
    return redirect('account_activation_sent')

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

# Password Reset Views
password_reset_view = PasswordResetView.as_view(
    template_name='password_reset_form.html',  # Use a custom template for the reset form
    email_template_name='password_reset_email.html',  # Use a custom email template
    success_url='/password_reset/done/',  # Redirect to this URL after a successful reset request
)

password_reset_done_view = PasswordResetDoneView.as_view(
    template_name='password_reset_done.html',  # Use a custom template for the "reset done" page
)

password_reset_confirm_view = PasswordResetConfirmView.as_view(
    template_name='password_reset_confirm.html',  # Use a custom template for the password reset form
    success_url='/reset/done/',  # Redirect to this URL after a successful password reset
)

password_reset_complete_view = PasswordResetCompleteView.as_view(
    template_name='password_reset_complete.html',  # Use a custom template for the "reset complete" page
)

