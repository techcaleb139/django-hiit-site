import re
import os

with open('templates/posts.html', 'r', encoding='utf-8') as f:
    posts_content = f.read()

style_match = re.search(r'<style>.*?</style>', posts_content, re.DOTALL)
style_content = style_match.group(0) if style_match else ''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Students List</title>
    {style_content}
</head>
<body>
    <div class="container">
        <header class="topbar">
            <div class="brand">Students List</div>
            <nav class="nav">
                <a href="/" class="active-nav">Home</a>
                <a href="{{% url 'add_student' %}}">Add Student</a>
            </nav>
        </header>

        <section class="page active">
            <div class="card-grid">
                {{% for student in students %}}
                <article class="post-card">
                    <div class="post-card-inner">
                        <span class="tag">ID: {{{{ student.student_id }}}}</span>
                        <h4>{{{{ student.first_name }}}} {{{{ student.last_name }}}}</h4>
                    </div>
                </article>
                {{% endfor %}}
            </div>
        </section>
    </div>
</body>
</html>'''

with open('templates/students.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Created students.html')
