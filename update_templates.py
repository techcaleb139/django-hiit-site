import os

TEMPLATES = {
    'templates/students.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Students List</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container">
        <header class="topbar">
            <div class="brand">Students List</div>
            <nav class="nav">
                <a href="/" class="active-nav">Home</a>
                <a href="{% url 'add_student' %}">Add Student</a>
            </nav>
        </header>

        <section class="page active">
            {% for message in messages %}
                <div class="message message-success">{{ message }}</div>
            {% endfor %}
            <div class="flex-between mb-4">
                <h2 class="mb-0">Students <span class="text-muted" style="font-size: 1rem;">({{ students.count }})</span></h2>
                <a href="{% url 'add_student' %}" class="btn btn-primary btn-inline btn-sm">Add student</a>
            </div>
            
            <div class="card" style="padding: 0; overflow: hidden;">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Phone Number</th>
                                <th>Description</th>
                                <th style="text-align: right;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for student in students %}
                            <tr>
                                <td>{{ student.first_name }}</td>
                                <td>{{ student.last_name }}</td>
                                <td class="text-muted">{{ student.phone_number }}</td>
                                <td class="text-muted">{{ student.description|truncatechars:30 }}</td>
                                <td>
                                    <div class="table-actions">
                                        <a href="{% url 'edit_student' student.pk %}" class="action-link action-edit">Edit</a>
                                        <form method="post" action="{% url 'delete_student' student.pk %}" onsubmit="return confirm('Delete this student?')">
                                            {% csrf_token %}
                                            <button type="submit" class="action-link action-delete">Delete</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% if not students %}
                <div class="empty-state">No students found.</div>
                {% endif %}
            </div>
        </section>
    </div>
</body>
</html>''',

    'templates/post_form.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Post</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container container-sm page-center">
        <div class="card" style="width: 100%;">
            <h1 class="text-center mb-4">Post Details</h1>
            <form action="" method="post">
                {% csrf_token %}
                {{post_form.as_p}}
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>''',

    'templates/add_student.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if student %}Edit Student{% else %}Add Student{% endif %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container container-sm page-center">
        <div class="card" style="width: 100%;">
            <h1 class="text-center mb-4">{% if student %}Edit Student{% else %}Add Student{% endif %}</h1>
            
            {% for message in messages %}
                <div class="message message-error">{{ message }}</div>
            {% endfor %}
            
            <form action="{% if student %}{% url 'edit_student' student.pk %}{% else %}{% url 'add_student' %}{% endif %}" method="post">
                {% csrf_token %}

                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" id="first_name" name="first_name" required placeholder="Enter first name" value="{{ student.first_name|default:'' }}">
                </div>

                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" id="last_name" name="last_name" required placeholder="Enter last name" value="{{ student.last_name|default:'' }}">
                </div>

                <div class="form-group">
                    <label for="student_id">Student ID</label>
                    <input type="text" id="student_id" name="student_id" required placeholder="Enter student ID (numbers only)" value="{{ student.student_id|default:'' }}">
                </div>

                <div class="form-group">
                    <label for="phone_number">Phone Number</label>
                    <input type="tel" id="phone_number" name="phone_number" placeholder="Enter phone number" value="{{ student.phone_number|default:'' }}">
                </div>

                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" name="description" placeholder="Enter description" rows="3">{{ student.description|default:'' }}</textarea>
                </div>

                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">{% if student %}Update Student{% else %}Add Student{% endif %}</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>''',

    'templates/create_user.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create User</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container container-sm page-center">
        <div class="card" style="width: 100%;">
            <h1 class="text-center mb-4">Create an Account</h1>
            
            {% for message in messages %}
                <div class="message message-error">{{ message }}</div>
            {% endfor %}

            <form action="{% url 'create_user' %}" method="post">
                {% csrf_token %}
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>

                <div class="form-group">
                    <label for="password_confirm">Confirm Password</label>
                    <input type="password" id="password_confirm" name="password_confirm" required>
                </div>

                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Sign Up</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>''',

    'templates/custom_create_user.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Create User</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container container-sm page-center">
        <div class="card" style="width: 100%;">
            <h1 class="text-center mb-4">Create User (Custom)</h1>
            
            {% for message in messages %}
                <div class="message message-error">{{ message }}</div>
            {% endfor %}

            <form action="{% url 'customer_create_user' %}" method="post">
                {% csrf_token %}

                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>

                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Sign Up</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>''',

    'templates/user_form.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Information Form</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container container-sm page-center">
        <div class="card" style="width: 100%;">
            <h1 class="text-center mb-4">User Information Form</h1>
            
            <form action="{% url 'submit_form' %}" method="post">
                {% csrf_token %}

                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" id="first_name" name="first_name" required>
                </div>

                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" id="last_name" name="last_name" required>
                </div>

                <div class="form-group">
                    <label for="age">Age</label>
                    <input type="number" id="age" name="age" required>
                </div>

                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>''',

    'templates/user_info.html': '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submitted User Information</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
    <div class="container container-sm page-center">
        <div class="card text-center" style="width: 100%;">
            <h1 class="mb-4">Submitted User Information</h1>
            
            <ul class="styled-list mb-4">
                <li><span class="text-muted">First Name:</span> <strong>{{ first_name }}</strong></li>
                <li><span class="text-muted">Last Name:</span> <strong>{{ last_name }}</strong></li>
                <li><span class="text-muted">Age:</span> <strong>{{ age }}</strong></li>
            </ul>

            <div class="flex-between" style="justify-content: center;">
                <a href="{% url 'home' %}" class="btn btn-secondary btn-inline">Go Back to Home</a>
            </div>
        </div>
    </div>
</body>
</html>'''
}

for path, content in TEMPLATES.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {path}')
