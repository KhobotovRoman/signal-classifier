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

# Загружаем файлы, исключая скрытые и чувствительные
def should_ignore(file_path):
    ignore_ext = ['.pyc', '.pyo']
    ignore_names = ['.DS_Store', '.env', '.gitignore', '__pycache__']
    return any(x in file_path for x in ignore_names) or any(file_path.endswith(ext) for ext in ignore_ext) or file_path.startswith(".")

def upload_dir_to_github(local_path, remote_path=""):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), local_path)
            if should_ignore(rel_path):
                print(f"⏭ Пропущен (игнор): {rel_path}")
                continue
            with open(os.path.join(root, file), "rb") as f:
                content = f.read()
            try:
                repo.create_file(os.path.join(remote_path, rel_path), f"Add {rel_path}", content, branch="main")
                print(f"📤 Добавлен: {rel_path}")
            except Exception as e:
                print(f"⚠️ Пропущен {rel_path}: {e}")

upload_dir_to_github(".", "")