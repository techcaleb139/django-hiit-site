with open('projectapp/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_string = 'from django.contrib.auth.decorators import login_required\n'
if 'login_required' not in content:
    content = content.replace('from django.contrib.auth import authenticate, login', 'from django.contrib.auth import authenticate, login\n' + import_string)
    
    # Decorate some views
    content = content.replace('def add_student(request):', '@login_required(login_url="login")\ndef add_student(request):')
    content = content.replace('def edit_student(request, pk):', '@login_required(login_url="login")\ndef edit_student(request, pk):')
    content = content.replace('def delete_student(request, pk):', '@login_required(login_url="login")\ndef delete_student(request, pk):')
    content = content.replace('def add_post(request):', '@login_required(login_url="login")\ndef add_post(request):')
    content = content.replace('def edit_post(request, pk):', '@login_required(login_url="login")\ndef edit_post(request, pk):')

    with open('projectapp/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
