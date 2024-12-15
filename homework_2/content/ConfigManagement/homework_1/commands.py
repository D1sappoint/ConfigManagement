import os

class Commands:
    def __init__(self, emulator):
        self.emulator = emulator

    def ls(self, args):
        node = self.get_current_node()
        if node is None:
            return f"ls: cannot access '{self.emulator.current_path}': No such directory"
        files = node.keys()
        return '  '.join(files)

    def cd(self, args):
        if not args:
            return ''
        path = args[0]
        if path == '/':
            self.emulator.current_path = '/'
            return ''
        parts = path.strip('/').split('/')
        node = self.emulator.vfs_tree
        for part in parts:
            if part == '..':
                self.emulator.current_path = os.path.dirname(os.path.dirname(self.emulator.current_path)) + '/'
                return ''
            if part not in node:
                return f"cd: {path}: No such directory"
            node = node[part]
        self.emulator.current_path = os.path.join(self.emulator.current_path, path) + '/'
        return ''

    def echo(self, args):
        return ' '.join(args)

    def rev(self, args):
        text = ' '.join(args)
        return text[::-1]

    def get_current_node(self):
        if self.emulator.current_path == '/':
            return self.emulator.vfs_tree
        parts = self.emulator.current_path.strip('/').split('/')
        node = self.emulator.vfs_tree
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None
        return node