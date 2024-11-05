from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

from django.http import HttpResponse

from django.contrib.auth.models import User

# Function to render the homepage
def home(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'webapp/index.html')  # Render the homepage template


# Function to handle user registration
def register(request):

    form = CreateUserForm()  # Instantiate an empty user creation form
    
    if request.method == "POST":  # Check if the form has been submitted

        form = CreateUserForm(request.POST)  # Populate the form with submitted data

        if form.is_valid():  # Validate the form

            form.save()  # Save the new user to the database

            messages.success(request, "Account created successfully")  # Display success message

            return redirect("my-login")  # Redirect to the login page

    context = {'form': form}  # Pass the form to the template context

    return render(request, 'webapp/register.html', context=context)  # Render the registration template


# Function to handle user login
def my_login(request):

    form = LoginForm()  # Instantiate an empty login form

    if request.method == "POST":  # Check if the form has been submitted

        form = LoginForm(request, data=request.POST)  # Populate the form with submitted data

        if form.is_valid():  # Validate the form

            username = request.POST.get('username')  # Get the submitted username
            password = request.POST.get('password')  # Get the submitted password

            user = authenticate(request, username=username, password=password)  # Authenticate the user

            if user is not None:  # Check if authentication was successful

                auth.login(request, user)  # Log in the user

                # Store user-specific data in session
                request.session['username'] = username

                # Set a cookie with the username
                response = redirect('dashboard')
                response.set_cookie('username', username, max_age=3600)  # Cookie expires in 1 hour

                messages.success(request, "You have logged in")  # Display success message
                return response  # Redirect to the dashboard

    context = {'form': form}  # Pass the form to the template context

    return render(request, 'webapp/my-login.html', context=context)  # Render the login template


# Function to render the dashboard, requiring user to be logged in
@login_required(login_url='my-login')
def dashboard(request):
    # Retrieve user-specific data from session
    username = request.session.get('username')

    # Get the username from the cookie
    cookie_username = request.COOKIES.get('username')

    my_records = Record.objects.all()  # Retrieve all records from the database

    context = {'records': my_records, 'username': username, 'cookie_username': cookie_username}  # Pass data to the template context

    return render(request, 'webapp/dashboard.html', context=context)  # Render the dashboard template


# Function to create a new record, requiring user to be logged in
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()  # Instantiate an empty record creation form

    if request.method == "POST":  # Check if the form has been submitted

        form = CreateRecordForm(request.POST)  # Populate the form with submitted data

        if form.is_valid():  # Validate the form

            form.save()  # Save the new record to the database

            messages.success(request, "Your record was created")  # Display success message
            return redirect("dashboard")  # Redirect to the dashboard

    context = {'form': form}  # Pass the form to the template context

    return render(request, 'webapp/create-record.html', context=context)  # Render the record creation template


# Function to update an existing record, requiring user to be logged in
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)  # Retrieve the record to be updated by its primary key

    form = UpdateRecordForm(instance=record)  # Instantiate a form with the existing record data

    if request.method == 'POST':  # Check if the form has been submitted

        form = UpdateRecordForm(request.POST, instance=record)  # Populate the form with submitted data

        if form.is_valid():  # Validate the form

            form.save()  # Save the updated record to the database

            messages.success(request, "Your record was updated")  # Display success message

            return redirect("dashboard")  # Redirect to the dashboard

    context = {'form': form}  # Pass the form to the template context

    return render(request, 'webapp/update-record.html', context=context)  # Render the record update template


# Function to view a singular record, requiring user to be logged in
@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)  # Retrieve the record by its primary key

    context = {'record': all_records}  # Pass the record to the template context

    return render(request, 'webapp/view-record.html', context=context)  # Render the record view template


# Function to delete a record, requiring user to be logged in
@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)  # Retrieve the record to be deleted by its primary key

    record.delete()  # Delete the record from the database

    messages.success(request, "Your record was deleted!")  # Display success message

    return redirect("dashboard")  # Redirect to the dashboard


#user logout

def user_logout(request):

    auth.logout(request)  # Log out the user

    # Clear all session data
    request.session.flush()

    # Delete the username cookie
    response = redirect("my-login")
    response.delete_cookie('username')

    messages.success(request, "Logout success!")  # Display success message
    return response 

