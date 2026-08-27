import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

nav_code = '''            <nav class="nav">
                {% if user.is_authenticated %}
                <span class="text-muted" style="padding: 8px 16px;">Hi, {{ user.username }}</span>
                <a href="{% url 'logout' %}">Logout</a>
                {% else %}
                <a href="{% url 'login' %}">Login</a>
                {% endif %}
                <a href="{% url 'about' %}">About</a>
                <a href="{% url 'posts' %}">Posts</a>
                <a href="{% url 'students' %}">Students</a>
            </nav>'''
            
content = re.sub(r'<nav class="nav">.*?</nav>', nav_code, content, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
