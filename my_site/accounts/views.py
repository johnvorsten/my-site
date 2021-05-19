from django.shortcuts import render, redirect, reverse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views

# Create your views here.
# Create instance of form in view
# Send instance of from to template so it can be sent to client
def signup_view(request):

    # This is how we handle get and post requests form the user
    # The user sends a 'get' request when they request a web page
    # When they send username and login info to create a user account they 
    # Are sending a 'post' request..
    if request.method == 'POST':
        # Validate user data (password match, existing user, etc)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save form to database
            form.save()
            # Log user in
            request_context = RequestContext(request)
            return render(request, 'accounts/signup_done.html', context={'name':name})

    else: # Get request
        # Return the form
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', context={'form':form})

# def signup_done_view(request, name=''):


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login_template.html'

def login_success_view(request):
    request_context = RequestContext(request)
    return render(request, 'accounts/login_done_template.html', context={})

class LogoutView(auth_views.LogoutView):
    # URL to redirect to after logout
    # next_page =  # Defaults to settings.LOGOUT_REDIRECT_URL
    template_name =  'accounts/logout_successful.html'

class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    # success_url = #

class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'