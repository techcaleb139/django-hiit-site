import re

with open('templates/students.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Nav
nav_code = '''            <nav class="nav">
                <a href="/" class="active-nav">Home</a>
                {% if user.is_authenticated %}
                <span class="text-muted" style="padding: 8px 16px;">Hi, {{ user.username }}</span>
                <a href="{% url 'logout' %}">Logout</a>
                {% else %}
                <a href="{% url 'login' %}">Login</a>
                {% endif %}
            </nav>'''
content = re.sub(r'<nav class="nav">.*?</nav>', nav_code, content, flags=re.DOTALL)

# Update Add Student button
content = content.replace('<a href="{% url \'add_student\' %}" class="btn btn-primary btn-inline btn-sm">Add student</a>', '{% if user.is_authenticated %}<a href="{% url \'add_student\' %}" class="btn btn-primary btn-inline btn-sm">Add student</a>{% endif %}')

# Update Header Actions
content = content.replace('<th style="text-align: right;">Actions</th>', '{% if user.is_authenticated %}<th style="text-align: right;">Actions</th>{% endif %}')

# Update Row Actions
row_actions = '''{% if user.is_authenticated %}
                                <td>
                                    <div class="table-actions">
                                        <a href="{% url 'edit_student' student.pk %}" class="action-link action-edit">Edit</a>
                                        <a href="{% url 'delete_student' student.pk %}" class="action-link action-delete">Delete</a>
                                    </div>
                                </td>
                                {% endif %}'''
content = re.sub(r'<td>\s*<div class="table-actions">.*?</div>\s*</td>', row_actions, content, flags=re.DOTALL)

# Update Colspan
content = content.replace('colspan="5"', 'colspan="{% if user.is_authenticated %}5{% else %}4{% endif %}"')

with open('templates/students.html', 'w', encoding='utf-8') as f:
    f.write(content)
