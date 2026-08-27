import os
import django
import sys
from bs4 import BeautifulSoup
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classproject.settings')
django.setup()

client = Client()

print("=====================")
print("TEST 1")
print("=====================")
# 1. Go to /posts/add/. Submit the form with the "name" field left blank.
response1 = client.post('/posts/add/', {'body': 'test body'})
print(f"Status Code: {response1.status_code}")
soup1 = BeautifulSoup(response1.content, 'html.parser')
body_textarea = soup1.find('textarea', {'name': 'body'})
if body_textarea:
    print(f"Data survived: body == '{body_textarea.text.strip()}'")
else:
    print("Data survived: No body textarea found.")

name_errors = soup1.select('ul.errorlist')
print(f"Validation error shown: {[e.text.strip() for e in name_errors] if name_errors else 'No error'}")

print("\n=====================")
print("TEST 2")
print("=====================")
# 2. Go to /posts/<id>/edit/ for an existing post. Change the name and submit.
from projectapp.models import Post, Student
from django.contrib.auth.models import User

# Make sure a post exists
p = Post.objects.first()
if not p:
    p = Post.objects.create(name='Original Name', body='Original Body')
response2 = client.post(f'/posts/{p.id}/edit/', {'name': 'Updated Name', 'body': p.body})
print(f"Redirected: {response2.status_code == 302}")
if response2.status_code == 302:
    print(f"Redirect URL: {response2.url}")
    resp2_follow = client.get(response2.url)
    print(f"Is 'Updated Name' in /posts/: {'Updated Name' in str(resp2_follow.content)}")

print("\n=====================")
print("TEST 3")
print("=====================")
# 3. Go to /user/create. Submit with password and password confirmation different.
response3 = client.post('/user/create', {
    'username': 'testuser1',
    'password': 'Password123!',
    'password_confirmation': 'Password321!' # Wait, django UserCreationForm uses specific field names? Actually let's just submit something random, wait, let's look at what fields UserCreationForm uses. Usually it is username, password, maybe not password_confirmation but password1 and password1? Wait, UserCreationForm uses 'username', 'password', 'password1', 'password1_confirmation'? Actually just username, password... let's check what default Django UserCreationForm fields are... wait, it doesn't matter, we can just submit mismatched passwords using the built-in form's fields if we know them. Or just submit an empty dict and see if form re-shows with errors. 
    # Actually, UserCreationForm fields are usually username, password (not sure). Let's fetch the form first.
})
resp3_get = client.get('/user/create')
soup3_get = BeautifulSoup(resp3_get.content, 'html.parser')
fields = [i.get('name') for i in soup3_get.find_all('input') if i.get('name')]
# Try to post mismatched passwords based on the fields found in the GET request.
# Django's UserCreationForm uses 'username', 'password', maybe we just submit something invalid.
post_data = {}
for f in fields:
    if f != 'csrfmiddlewaretoken':
        post_data[f] = 'pw1' if '1' in f else ('pw2' if '2' in f else 'testuser1')

response3 = client.post('/user/create', post_data)
soup3 = BeautifulSoup(response3.content, 'html.parser')
errors3 = soup3.select('ul.errorlist')
print(f"Errors visible: {[e.text.strip() for e in errors3] if errors3 else 'None'}")


print("\n=====================")
print("TEST 4")
print("=====================")
# 4. Go to /user/create. Submit valid, unique signup data.
import random
username4 = f"user_{random.randint(1000, 9999)}"
# Getting actual field names is safer
post_data4 = {}
for f in fields:
    if f == 'username':
        post_data4[f] = username4
    elif 'password' in f or 'pw' in f:
        post_data4[f] = 'TestPassword123!'
    elif f != 'csrfmiddlewaretoken':
        post_data4[f] = 'test'
response4 = client.post('/user/create', post_data4)
print(f"Redirected: {response4.status_code == 302}, Target: {response4.url if response4.status_code == 302 else 'None'}")
print(f"User created: {User.objects.filter(username=username4).exists()}")


print("\n=====================")
print("TEST 5")
print("=====================")
# 5. Go to /user/create-custom/. Submit with password and confirm_password different.
response5 = client.post('/user/create-custom/', {
    'username': 'customuser1',
    'email': 'custom1@example.com',
    'password': 'pwd1',
    'confirm_password': 'pwd2'
})
print(f"Redirected: {response5.status_code == 302}, Target: {response5.url if response5.status_code == 302 else 'None'}")
if response5.status_code == 302:
    resp5_follow = client.get(response5.url)
    soup5 = BeautifulSoup(resp5_follow.content, 'html.parser')
    err5 = soup5.find('p', style=lambda value: value and 'color:red' in value)
    print(f"Error message shown: {err5.text.strip() if err5 else 'None'}")

print("\n=====================")
print("TEST 6")
print("=====================")
# 6. Go to /user/create-custom/. Submit with a username that already exists (reuse the one from test 4).
response6 = client.post('/user/create-custom/', {
    'username': username4, # Reusing username from Test 4
    'email': 'custom2@example.com',
    'password': 'pwd1',
    'confirm_password': 'pwd1'
})
if response6.status_code == 302:
    resp6_follow = client.get(response6.url)
    soup6 = BeautifulSoup(resp6_follow.content, 'html.parser')
    err6 = soup6.find('p', style=lambda value: value and 'color:red' in value)
    print(f"Error message shown: {err6.text.strip() if err6 else 'None'}")


print("\n=====================")
print("TEST 7")
print("=====================")
# 7. Go to /user/create-custom/. Submit fresh, valid, unique data.
username7 = f"custom_{random.randint(1000, 9999)}"
response7 = client.post('/user/create-custom/', {
    'username': username7,
    'email': 'custom7@example.com',
    'password': 'TestPassword123!',
    'confirm_password': 'TestPassword123!'
})
print(f"Redirected: {response7.status_code == 302}, Target: {response7.url if response7.status_code == 302 else 'None'}")
print(f"User created: {User.objects.filter(username=username7).exists()}")


print("\n=====================")
print("TEST 8")
print("=====================")
# 8. Go to /student/add/. Submit with the Student ID field set to "abc" (non-numeric).
try:
    response8 = client.post('/student/add/', {
        'first_name': 'John',
        'last_name': 'Doe',
        'student_id': 'abc'
    })
    print(f"Status Code: {response8.status_code}")
    soup8 = BeautifulSoup(response8.content, 'html.parser')
    err8 = soup8.find('p', style=lambda value: value and 'color:red' in value)
    print(f"Error message shown: {err8.text.strip() if err8 else 'None'}")
except Exception as e:
    print(f"Crashed with exception: {e}")

print("\n=====================")
print("TEST 9")
print("=====================")
# 9. Go to /student/add/. Submit valid data, then submit the exact same Student ID again.
std_id = random.randint(10000, 99999)
client.post('/student/add/', {
    'first_name': 'Jane',
    'last_name': 'Doe',
    'student_id': str(std_id)
})
# Submit again
try:
    response9 = client.post('/student/add/', {
        'first_name': 'Jim',
        'last_name': 'Doe',
        'student_id': str(std_id)
    })
    print(f"Status Code (2nd submit): {response9.status_code}")
    soup9 = BeautifulSoup(response9.content, 'html.parser')
    err9 = soup9.find('p', style=lambda value: value and 'color:red' in value)
    print(f"Error message shown: {err9.text.strip() if err9 else 'None'}")
except Exception as e:
    print(f"Crashed with exception: {e}")

print("\n=====================")
print("TEST 10")
print("=====================")
# 10. Go to /student/add/. Submit fresh, valid, unique data.
initial_count = Student.objects.count()
std_id10 = random.randint(10000, 99999)
response10 = client.post('/student/add/', {
    'first_name': 'Alice',
    'last_name': 'Smith',
    'student_id': str(std_id10)
})
print(f"Redirected: {response10.status_code == 302}, Target: {response10.url if response10.status_code == 302 else 'None'}")
final_count = Student.objects.count()
print(f"Student count: {final_count} (Increased by {final_count - initial_count})")

