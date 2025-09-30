import os
import re
from flask import Flask, render_template, request, jsonify, send_file
from github import Github
import requests
from io import BytesIO
import markdown

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET')
if not app.secret_key:
    raise ValueError("SESSION_SECRET environment variable is required")

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

def get_github_client():
    if GITHUB_TOKEN:
        return Github(GITHUB_TOKEN)
    return Github()

def parse_github_url(url):
    patterns = [
        r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
        r'github\.com/([^/]+)/([^/]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
    return None, None

def detect_tech_stack(repo):
    tech_stack = []
    instructions = []
    
    try:
        contents = repo.get_contents("")
        file_names = [content.name for content in contents]
        
        if 'package.json' in file_names:
            node_frameworks = []
            try:
                import json
                pkg_json = repo.get_contents("package.json").decoded_content.decode()
                pkg_data = json.loads(pkg_json)
                deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                
                if 'express' in deps:
                    node_frameworks.append('Express')
                if 'next' in deps:
                    node_frameworks.append('Next.js')
                if 'react' in deps:
                    node_frameworks.append('React')
                if 'vue' in deps:
                    node_frameworks.append('Vue')
                if 'vite' in deps:
                    node_frameworks.append('Vite')
            except:
                pass
            
            tech_stack.append('Node.js')
            if node_frameworks:
                tech_stack.extend(node_frameworks)
            
            instructions.extend([
                f'# Node.js Setup {("(" + ", ".join(node_frameworks) + ")") if node_frameworks else ""}',
                '```bash',
                'npm install',
                'npm start',
                '# or',
                'npm run dev',
                '```'
            ])
        
        if 'requirements.txt' in file_names or 'setup.py' in file_names or 'pyproject.toml' in file_names:
            py_frameworks = []
            try:
                if 'requirements.txt' in file_names:
                    req_txt = repo.get_contents("requirements.txt").decoded_content.decode().lower()
                    if 'django' in req_txt:
                        py_frameworks.append('Django')
                    if 'flask' in req_txt:
                        py_frameworks.append('Flask')
                    if 'fastapi' in req_txt:
                        py_frameworks.append('FastAPI')
            except:
                pass
            
            tech_stack.append('Python')
            if py_frameworks:
                tech_stack.extend(py_frameworks)
            
            framework_cmd = ''
            if 'Django' in py_frameworks:
                framework_cmd = 'python manage.py runserver'
            elif 'Flask' in py_frameworks:
                framework_cmd = 'flask run'
            elif 'FastAPI' in py_frameworks:
                framework_cmd = 'uvicorn main:app --reload'
            else:
                framework_cmd = 'python app.py'
            
            instructions.extend([
                f'# Python Setup {("(" + ", ".join(py_frameworks) + ")") if py_frameworks else ""}',
                '```bash',
                'pip install -r requirements.txt',
                framework_cmd,
                '```'
            ])
        
        if 'Dockerfile' in file_names:
            tech_stack.append('Docker')
            instructions.extend([
                '# Docker Setup',
                '```bash',
                'docker build -t app .',
                'docker run -p 8080:8080 app',
                '```'
            ])
        
        if 'go.mod' in file_names:
            tech_stack.append('Go')
            instructions.extend([
                '# Go Setup',
                '```bash',
                'go mod download',
                'go run main.go',
                '# or',
                'go build && ./app',
                '```'
            ])
        
        if 'pom.xml' in file_names or 'build.gradle' in file_names:
            java_frameworks = []
            try:
                if 'pom.xml' in file_names:
                    pom = repo.get_contents("pom.xml").decoded_content.decode().lower()
                    if 'spring-boot' in pom:
                        java_frameworks.append('Spring Boot')
            except:
                pass
            
            tech_stack.append('Java')
            if java_frameworks:
                tech_stack.extend(java_frameworks)
            
            if 'Spring Boot' in java_frameworks:
                instructions.extend([
                    f'# Java Setup (Spring Boot)',
                    '```bash',
                    'mvn clean install && mvn spring-boot:run',
                    '# or for Gradle',
                    'gradle build && gradle bootRun',
                    '```'
                ])
            else:
                instructions.extend([
                    f'# Java Setup',
                    '```bash',
                    'mvn clean package && java -jar target/*.jar',
                    '# or for Gradle',
                    'gradle build && java -jar build/libs/*.jar',
                    '```'
                ])
        
        if 'Gemfile' in file_names:
            ruby_frameworks = []
            try:
                gemfile = repo.get_contents("Gemfile").decoded_content.decode().lower()
                if 'rails' in gemfile:
                    ruby_frameworks.append('Rails')
            except:
                pass
            
            tech_stack.append('Ruby')
            if ruby_frameworks:
                tech_stack.extend(ruby_frameworks)
            
            cmd = 'rails server' if 'Rails' in ruby_frameworks else 'ruby app.rb'
            instructions.extend([
                f'# Ruby Setup {("(" + ", ".join(ruby_frameworks) + ")") if ruby_frameworks else ""}',
                '```bash',
                'bundle install',
                cmd,
                '```'
            ])
        
        if 'Cargo.toml' in file_names:
            tech_stack.append('Rust')
            instructions.extend([
                '# Rust Setup',
                '```bash',
                'cargo build',
                'cargo run',
                '```'
            ])
        
        if 'composer.json' in file_names:
            php_frameworks = []
            try:
                composer = repo.get_contents("composer.json").decoded_content.decode().lower()
                if 'laravel' in composer:
                    php_frameworks.append('Laravel')
            except:
                pass
            
            tech_stack.append('PHP')
            if php_frameworks:
                tech_stack.extend(php_frameworks)
            
            cmd = 'php artisan serve' if 'Laravel' in php_frameworks else 'php -S localhost:8000'
            instructions.extend([
                f'# PHP Setup {("(" + ", ".join(php_frameworks) + ")") if php_frameworks else ""}',
                '```bash',
                'composer install',
                cmd,
                '```'
            ])
        
        if '.env.example' in file_names or '.env.sample' in file_names:
            instructions.insert(0, '⚠️ **Important**: Copy `.env.example` to `.env` and configure environment variables before running.')
        
        if not tech_stack:
            tech_stack.append('Unknown')
            instructions.append('# Check the README for setup instructions')
        
    except Exception as e:
        tech_stack.append('Unable to detect')
        instructions.append(f'# Error: {str(e)}')
    
    return tech_stack, '\n'.join(instructions)

def sanitize_mermaid_text(text):
    return (text.replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;')
                .replace('[', '&#91;')
                .replace(']', '&#93;'))

def generate_mermaid_diagram(repo):
    try:
        contents = repo.get_contents("")
        file_structure = {}
        
        for content in contents[:20]:
            if content.type == "dir":
                file_structure[content.name] = "directory"
            else:
                file_structure[content.name] = "file"
        
        mermaid = "graph TD\n"
        mermaid += f"    Root[{sanitize_mermaid_text(repo.name)}]\n"
        
        for idx, (name, ftype) in enumerate(file_structure.items()):
            node_id = f"Node{idx}"
            sanitized_name = sanitize_mermaid_text(name)
            if ftype == "directory":
                mermaid += f"    {node_id}[📁 {sanitized_name}]\n"
            else:
                ext = name.split('.')[-1] if '.' in name else 'file'
                icon = {
                    'py': '🐍',
                    'js': '📜',
                    'json': '📋',
                    'md': '📝',
                    'html': '🌐',
                    'css': '🎨',
                    'go': '🔵',
                    'rs': '🦀',
                    'java': '☕',
                    'rb': '💎',
                }.get(ext, '📄')
                mermaid += f"    {node_id}[{icon} {sanitized_name}]\n"
            mermaid += f"    Root --> {node_id}\n"
        
        return mermaid
    except Exception as e:
        sanitized_error = sanitize_mermaid_text(str(e))
        return f"graph TD\n    Root[{sanitize_mermaid_text(repo.name)}]\n    Error[Could not generate diagram: {sanitized_error}]"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    repo_url = data.get('repo_url', '').strip()
    
    if not repo_url:
        return jsonify({'error': 'Please provide a GitHub repository URL'}), 400
    
    owner, repo_name = parse_github_url(repo_url)
    
    if not owner or not repo_name:
        return jsonify({'error': 'Invalid GitHub URL format. Use: https://github.com/owner/repo'}), 400
    
    try:
        g = get_github_client()
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        tech_stack, instructions = detect_tech_stack(repo)
        mermaid_diagram = generate_mermaid_diagram(repo)
        
        replit_url = f"https://replit.com/github/{owner}/{repo_name}"
        
        result = {
            'repo_name': repo.name,
            'description': repo.description or 'No description available',
            'owner': owner,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'language': repo.language or 'Not specified',
            'tech_stack': tech_stack,
            'instructions': instructions,
            'mermaid_diagram': mermaid_diagram,
            'replit_url': replit_url,
            'github_url': repo.html_url
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch repository: {str(e)}'}), 500

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    
    content = f"""# REPO_TOUR.md
# {data.get('repo_name', 'Repository')} - Quick Start Guide

## 📋 Repository Information
- **Name**: {data.get('repo_name', 'N/A')}
- **Owner**: {data.get('owner', 'N/A')}
- **Description**: {data.get('description', 'N/A')}
- **Primary Language**: {data.get('language', 'N/A')}
- **Stars**: ⭐ {data.get('stars', 0)}
- **Forks**: 🍴 {data.get('forks', 0)}
- **GitHub URL**: {data.get('github_url', 'N/A')}

## 🛠️ Tech Stack Detected
{', '.join(data.get('tech_stack', []))}

## 🚀 Quick Start Instructions

{data.get('instructions', 'No instructions available')}

## 📂 Repository Structure

```mermaid
{data.get('mermaid_diagram', 'No diagram available')}
```

## 🔗 Quick Links

- **Open in Replit**: {data.get('replit_url', 'N/A')}
- **GitHub Repository**: {data.get('github_url', 'N/A')}

---
*Generated by RepoStory - Making repositories judge-friendly*
"""
    
    buffer = BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='REPO_TOUR.md',
        mimetype='text/markdown'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
