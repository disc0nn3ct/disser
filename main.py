import git
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import shutil

# URL репозитория и путь для клонирования
# REPO_URL = 'https://github.com/owner/repo.git'
REPO_URL = 'https://github.com/disc0nn3ct/Tcam'
CLONE_PATH = 'D:/study/статьи/project/buffer'

def clone_repo(repo_url, clone_path):
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)  # Удаляем старый клон
    return git.Repo.clone_from(repo_url, clone_path)

def get_commit_code(repo, commit_sha):
    commit = repo.commit(commit_sha)
    code_files = []

    for item in commit.tree.traverse():
        if item.type == 'blob':  # Рассматриваем только файлы (blobs)
            file_content = item.data_stream.read().decode('utf-8', errors='ignore')
            code_files.append(file_content)
    
    return "\n".join(code_files)

def vectorize_code(codes):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(codes)
    return vectors.toarray()

def calculate_code_difference(vector1, vector2):
    return cosine(vector1, vector2)

def get_main_branch(repo):
    branches = [branch.name for branch in repo.branches]
    if 'master' in branches:
        return 'master'
    elif 'main' in branches:
        return 'main'
    else:
        raise ValueError("Не найдена ни ветка 'master', ни 'main'.")

def analyze_repo(repo_url, clone_path):
    repo = clone_repo(repo_url, clone_path)
    branch = get_main_branch(repo)
    commits = list(repo.iter_commits(branch, max_count=2))

    if len(commits) < 2:
        print("Недостаточно коммитов для анализа.")
        return

    old_commit_code = get_commit_code(repo, commits[1].hexsha)
    new_commit_code = get_commit_code(repo, commits[0].hexsha)

    vectors = vectorize_code([old_commit_code, new_commit_code])
    old_vector = vectors[0]
    new_vector = vectors[1]

    difference = calculate_code_difference(old_vector, new_vector)

    print(f"Изменение кода между коммитами {commits[1].hexsha} и {commits[0].hexsha}: {difference:.4f}")

if __name__ == '__main__':
    analyze_repo(REPO_URL, CLONE_PATH)




# import tempfile

# def clone_repo(repo_url):
#     clone_path = tempfile.mkdtemp()  # Создаем временную директорию для клонирования
#     return git.Repo.clone_from(repo_url, clone_path), clone_path

# def get_commit_code(repo, commit_sha):
#     commit = repo.commit(commit_sha)
#     code_files = []

#     for item in commit.tree.traverse():
#         if item.type == 'blob':  # Рассматриваем только файлы (blobs)
#             file_content = item.data_stream.read().decode('utf-8', errors='ignore')
#             code_files.append(file_content)
    
#     return "\n".join(code_files)

# def vectorize_code(codes):
#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform(codes)
#     return vectors.toarray()

# def calculate_code_difference(vector1, vector2):
#     return cosine(vector1, vector2)

# def get_main_branch(repo):
#     branches = [branch.name for branch in repo.branches]
#     if 'master' in branches:
#         return 'master'
#     elif 'main' in branches:
#         return 'main'
#     else:
#         raise ValueError("Не найдена ни ветка 'master', ни 'main'.")

# def analyze_repo(repo_url):
#     repo, clone_path = clone_repo(repo_url)
#     branch = get_main_branch(repo)
#     commits = list(repo.iter_commits(branch, max_count=2))

#     if len(commits) < 2:
#         print("Недостаточно коммитов для анализа.")
#         return

#     old_commit_code = get_commit_code(repo, commits[1].hexsha)
#     new_commit_code = get_commit_code(repo, commits[0].hexsha)

#     vectors = vectorize_code([old_commit_code, new_commit_code])
#     old_vector = vectors[0]
#     new_vector = vectors[1]

#     difference = calculate_code_difference(old_vector, new_vector)

#     print(f"Изменение кода между коммитами {commits[1].hexsha} и {commits[0].hexsha}: {difference:.4f}")

#     # Удаление временной директории
#     shutil.rmtree(clone_path)

# if __name__ == '__main__':
#     analyze_repo(REPO_URL)    