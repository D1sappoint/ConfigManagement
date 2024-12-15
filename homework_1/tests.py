import unittest
from shell_emulator import ShellEmulator
import os

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator('test_computer', 'virtual_filesystem.zip', 'test_log.json', None)
        self.emulator.load_vfs()

    def test_ls_root(self):
        output = self.emulator.commands.ls([])
        expected = 'bin  home  usr'
        self.assertEqual(output, expected)

    def test_cd_home(self):
        self.emulator.commands.cd(['home'])
        self.assertEqual(self.emulator.current_path, '/home/')

    def test_echo(self):
        output = self.emulator.commands.echo(['Hello,', 'World!'])
        expected = 'Hello, World!'
        self.assertEqual(output, expected)

    def test_rev(self):
        output = self.emulator.commands.rev(['abcde'])
        expected = 'edcba'
        self.assertEqual(output, expected)

    def test_cd_nonexistent(self):
        output = self.emulator.commands.cd(['nonexistent'])
        expected = 'cd: nonexistent: No such directory'
        self.assertEqual(output, expected)

    def test_ls_subdir(self):
        self.emulator.commands.cd(['home'])
        output = self.emulator.commands.ls([])
        expected = 'user'
        self.assertEqual(output, expected)

    def test_echo_empty(self):
        output = self.emulator.commands.echo([])
        expected = ''
        self.assertEqual(output, expected)

    def test_rev_sentence(self):
        output = self.emulator.commands.rev(['Hello,', 'World!'])
        expected = '!dlroW ,olleH'
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()