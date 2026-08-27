import os
import re

files = [
    'templates/index.html',
    'templates/about.html',
    'templates/posts.html',
    'templates/post.html',
    'templates/post_form.html',
    'templates/students.html',
    'templates/add_student.html',
    'templates/create_user.html',
    'templates/custom_create_user.html',
    'templates/user_form.html',
    'templates/user_info.html'
]

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add cache buster
        content = content.replace("href=\"{% static 'css/style.css' %}\"", "href=\"{% static 'css/style.css' %}?v=2\"")
        
        # Remove Goat image
        if 'images/Goat.jpg' in content:
            content = re.sub(r'<img[^>]*Goat\.jpg[^>]*>', '', content)
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Processed {file}')
