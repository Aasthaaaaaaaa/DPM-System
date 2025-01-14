from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import firestore

# Initialize Firestore DB
db = firestore.client()

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_type = request.POST['user_type']
        address_line1 = request.POST['address_line1']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        # Check if password and confirm password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if the user already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        # Create new user with address fields
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            address_line1=address_line1,
            city=city,
            state=state,
            pincode=pincode
        )

        # Create user in Firebase Firestore as well
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'user_type': user_type,
            'address_line1': address_line1,
            'city': city,
            'state': state,
            'pincode': pincode
        }
        db.collection('users').document(username).set(user_data)

        # Log the user in after successful signup
        login(request, user)

        # Show a success message
        messages.success(request, "Successfully signed up! Please login now.")

        # Don't redirect to the dashboard; stay on the signup page
        return render(request, 'signup.html')


    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            
            # Redirect to respective dashboard based on user type
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')  # Replace with your doctor's dashboard URL
            else:
                return redirect('patient_dashboard')  # Replace with your patient's dashboard URL
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')  # Redirect to login page in case of failure

    return render(request, 'login.html')


@login_required
def doctor_dashboard(request):
    # Add user to the context
    return render(request, 'doctor_dashboard.html', {'user': request.user})

@login_required
def patient_dashboard(request):
    # Add user to the context
    return render(request, 'patient_dashboard.html', {'user': request.user})

def logout_view(request):
    # Logout the user
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')  # Redirect to the login page after logout


from django.shortcuts import redirect

def landing_page(request):
    # Redirect to the signup page
    return redirect('signup')  # Make sure 'signup' is the correct name for your signup URL
