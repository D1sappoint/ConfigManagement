import unittest
import os
import subprocess
import graphviz
from IPython.display import display

def get_git_commits(repo_path):
    try:
        previous_cwd = os.getcwd()
        os.chdir(repo_path)
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%H|%P|%an|%ad'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
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

class TestVisualizer(unittest.TestCase):

    def test_build_graphviz_graph(self):
        commits = [
            'hash1|hash0|Author One|Date One',
            'hash2|hash1|Author Two|Date Two',
            'hash3|hash1 hash2|Author Three|Date Three',
            'hash0||Author Zero|Date Zero'
        ]
        dot = build_graphviz_graph(commits)
        dot_source = dot.source
        # Учитываем отступы
        self.assertIn('\thash1 [label="Author One\nDate One"]', dot_source)
        self.assertIn('\thash1 -> hash0', dot_source)
        self.assertIn('\thash2 [label="Author Two\nDate Two"]', dot_source)
        self.assertIn('\thash2 -> hash1', dot_source)
        self.assertIn('\thash3 [label="Author Three\nDate Three"]', dot_source)
        self.assertIn('\thash3 -> hash1', dot_source)
        self.assertIn('\thash3 -> hash2', dot_source)
        self.assertIn('\thash0 [label="Author Zero\nDate Zero"]', dot_source)

    def test_get_git_commits(self):
        # Укажите путь к вашему клонированному репозиторию
        repo_path = '/content/ConfigManagement/'  # Замените на ваш путь
        if not os.path.isdir(repo_path):
            self.fail(f"Репозиторий {repo_path} не найден.")
        commits = get_git_commits(repo_path)
        self.assertTrue(len(commits) > 0, "Функция get_git_commits не вернула коммиты.")
        first_commit = commits[0]
        parts = first_commit.split('|')
        self.assertTrue(len(parts) >= 4)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)