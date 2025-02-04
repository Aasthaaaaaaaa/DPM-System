from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Blog

def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  # Retrieve user_type from POST data

        # Validate user_type
        if user_type not in ['doctor', 'patient']:
            messages.error(request, "Invalid user type selected!")
            return redirect('signup')

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address_line1 = request.POST['address_line1']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        profile_picture = request.FILES.get('profile_picture')  # Get the profile picture from the form

        # Check if password and confirm password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if the user already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        # Create new user with address fields and profile picture
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
            pincode=pincode,
            profile_picture=profile_picture  # Save the profile picture
        )

        # Log the user in after successful signup
        login(request, user)

        # Show a success message
        messages.success(request, "Successfully signed up! Please login now.")

        # Redirect to the dashboard or a different page after signup
        return redirect('signup')  # Or the page you want to redirect to after signup

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


from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES.get('image')
        category = request.POST['category']
        summary = request.POST['summary']
        content = request.POST['content']
        is_draft = 'is_draft' in request.POST

        # Create and save the blog
        blog = Blog.objects.create(
            title=title,
            image=image,
            category=category,
            summary=summary,
            content=content,
            is_draft=is_draft,
            author=request.user  # Save the blog with the logged-in user
        )

        # Add a success message or redirect to the dashboard
        return render(request, 'create_blog.html', {'success_message': 'Blog created successfully!'})

    return render(request, 'create_blog.html')


@login_required
def doctor_blogs(request):
    if request.user.user_type == 'doctor':
        doctor_blogs = Blog.objects.filter(author=request.user)
        published_blogs = doctor_blogs.filter(is_draft=False)
        draft_blogs = doctor_blogs.filter(is_draft=True)
        context = {
            "published_blogs": published_blogs,
            "draft_blogs": draft_blogs,
        }
        return render(request, "doctor_blogs.html", context)
    else:
        return redirect("login")  # Redirect to login if not a doctor


@login_required
def patient_blogs(request):
    print(f"Logged-in User: {request.user.username}, User Type: {getattr(request.user, 'user_type', None)}")
    
    if hasattr(request.user, 'user_type') and request.user.user_type == 'patient':
        print("User is a patient.")
        # Fetch all non-draft blogs authored by doctors
        doctor_blogs = Blog.objects.filter(is_draft=False, author__user_type='doctor')
        blogs_by_category = {}
        for blog in doctor_blogs:
            category = blog.category  # Assuming 'category' is a field in Blog
            if category not in blogs_by_category:
                blogs_by_category[category] = []
            blogs_by_category[category].append(blog)

        context = {'blogs_by_category': blogs_by_category}
        return render(request, 'patient_blogs.html', context)

    print("User is not a patient. Redirecting to login.")
    return redirect('login')  # Redirect if user is not a patient


@login_required
def delete_blog(request, blog_id):
    if request.method == "POST":  # Ensure deletion only happens on POST request
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)  # Ensure the user is the owner
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")
    
    return redirect('doctor_blogs')  # Redirect to the list of blogs after deletion