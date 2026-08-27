with open('projectapp/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for authenticate and login
import_string = 'from django.contrib.auth import authenticate, login\n'
content = content.replace('from django.contrib.auth.models import User', 'from django.contrib.auth.models import User\n' + import_string)

# Add login view
login_view_code = '''
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    else:
        return render(request, "auth/login.html")
'''

content += login_view_code

with open('projectapp/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
