import subprocess
import os
import graphviz
from IPython.display import display

def get_git_commits(repo_path):
    try:
        # Сохраняем текущую директорию
        previous_cwd = os.getcwd()
        # Переходим в директорию репозитория
        os.chdir(repo_path)
        # Получаем список коммитов
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%H|%P|%an|%ad'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Возвращаемся в предыдущую директорию
        os.chdir(previous_cwd)
        if result.returncode != 0:
            print("Ошибка при выполнении git log:", result.stderr)
            return []
        return result.stdout.strip().split('\n')
    except Exception as e:
        print("Ошибка при получении коммитов:", e)
        return []

def build_graphviz_graph(commits):
    dot = graphviz.Digraph(comment='Git Commit Graph', format='png')
    for commit in commits:
        parts = commit.strip().split('|')
        commit_hash = parts[0]
        parents = parts[1].split()
        author = parts[2]
        date = parts[3]
        label = f"{author}\n{date}"
        dot.node(commit_hash, label=label)
        for parent in parents:
            if parent != '':
                dot.edge(commit_hash, parent)
    return dot

def visualize_graph(dot):
    # Отображаем граф в ноутбуке Colab
    display(dot)

# Укажите путь к вашему репозиторию
repo_path = '/content/ConfigManagement/'

commits = get_git_commits(repo_path)
if commits:
    dot = build_graphviz_graph(commits)
    visualize_graph(dot)
else:
    print("Нет коммитов для отображения.")