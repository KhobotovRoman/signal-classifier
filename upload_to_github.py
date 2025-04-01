import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
username = os.getenv("GITHUB_USERNAME")
repo_name = os.getenv("REPO_NAME")

g = Github(token)
user = g.get_user()
repo = None

try:
    repo = user.get_repo(repo_name)
    print(f"✅ Репозиторий уже существует: {repo.full_name}")
except:
    repo = user.create_repo(name=repo_name, private=False)
    print(f"📦 Репозиторий создан: {repo.full_name}")

# Загружаем файлы
import base64

def upload_dir_to_github(local_path, remote_path=""):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, local_path)
            if rel_path.startswith(".git") or rel_path.endswith(".pyc"):
                continue
            with open(path, "rb") as f:
                content = f.read()
            try:
                repo.create_file(os.path.join(remote_path, rel_path), f"Add {rel_path}", content, branch="main")
                print(f"📤 Добавлен: {rel_path}")
            except Exception as e:
                print(f"⚠️ Пропущен {rel_path}: {e}")

upload_dir_to_github(".", "")