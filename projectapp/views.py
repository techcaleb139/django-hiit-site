from multiprocessing import context

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from projectapp.models import Post, Student
from projectapp.forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth



from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, "index.html")

def about(request):
    about_message = "This is a message for the about page from the backend"

    best_players = ["Ororo", "Neymar", "Mbappe", "Dembele"]
    GOAT = "CR7"


    context = {"taofeek" : about_message, "programmer_name": "kaybobo", "programmer_age": "21", "best_players": best_players, "GOAT": GOAT }
    return render(request, "about.html", context)




def profile(request):
    me ={"name":"Caleb", "class": "Python", "age": 24}
    return JsonResponse(me)



def posts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "posts.html", context)


def post(request, pk):
    the_post = get_object_or_404(Post, pk=pk)
    context = {'post': the_post}
    return render(request, "post.html", context)


def user_form(request):
    return render(request, "user_form.html")



def submit_form(request):
    if request.method == "POST":

        name = request.POST.get("name")
        dept = request.POST.get("department")
        context = {"name": name, "department": dept}
        return JsonResponse(context)
    else:
        return redirect("user_form")


@login_required(login_url="login")
def add_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()

    context = {"post_form": form}
    return render(request, "post_form.html", context)

@login_required(login_url="login")
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("posts")

    else:
        form = PostForm(instance=post)

    context = {"post_form": form}
    return render(request, "post_form.html", context)

def create_user(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created. Please log in to continue.")
            return redirect("login")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "create_user.html", context)


def customer_create_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not (username and password and confirm_password):
            messages.error(request, "Please correct the error below.")
            return redirect("customer_create_user")
            
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("customer_create_user")

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
            return redirect("customer_create_user")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Your account has been successfully created. Please log in to continue.")
        return redirect("login")
    else:
        return render(request, "custom_create_user.html")

@login_required(login_url="login")
def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number", "")
        description = request.POST.get("description", "")

        if not (first_name and last_name):
            messages.error(request, "First and last name are required")
            return render(request, "add_student.html")

        # Auto-generate student_id
        from django.db.models import Max
        max_id = Student.objects.aggregate(Max('student_id'))['student_id__max']
        student_id = (max_id or 1000) + 1

        Student.objects.create(first_name=first_name, last_name=last_name, student_id=student_id, phone_number=phone_number, description=description)
        messages.success(request, "Student added successfully")
        return redirect("students")
    else:
        return render(request, "add_student.html")

def students(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, "students.html", context)

@login_required(login_url="login")
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number", "")
        description = request.POST.get("description", "")

        if not (first_name and last_name):
            messages.error(request, "First and last name are required")
            return render(request, "add_student.html", {"student": student})

        student.first_name = first_name
        student.last_name = last_name
        student.phone_number = phone_number
        student.description = description
        student.save()
        messages.success(request, "Student updated successfully")
        return redirect("students")
    else:
        return render(request, "add_student.html", {"student": student})

@login_required(login_url="login")
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted")
        return redirect("students")
    return render(request, "delete_student.html", {"student": student})
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            if next_url:
                return redirect(f"/login/?next={next_url}")
            return redirect("login")
    else:
        next_url = request.GET.get("next")
        return render(request, "auth/login.html", {"next": next_url})

def logout_view(request):
    logout(request)
    return redirect('home')
