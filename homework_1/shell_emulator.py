import sys
import argparse
import zipfile
import os
import json
import tkinter as tk
from tkinter import scrolledtext, END
from commands import Commands

class ShellEmulator:
    def __init__(self, computer_name, vfs_path, log_path, startup_script):
        self.computer_name = computer_name
        self.vfs_path = vfs_path
        self.log_path = log_path
        self.startup_script = startup_script
        self.current_path = '/'
        self.history = []
        self.log = []
        self.commands = Commands(self)
        self.load_vfs()

    def load_vfs(self):
        self.vfs = zipfile.ZipFile(self.vfs_path, 'r')
        self.vfs_tree = {}
        for file in self.vfs.namelist():
            parts = file.strip('/').split('/')
            node = self.vfs_tree
            for part in parts:
                node = node.setdefault(part, {})

    def save_log(self):
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(self.log, f, ensure_ascii=False, indent=4)

    def parse_command(self, command_line):
        self.history.append(command_line)
        parts = command_line.strip().split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]
        self.log.append({'command': command, 'args': args})
        if command == 'ls':
            output = self.commands.ls(args)
        elif command == 'cd':
            output = self.commands.cd(args)
        elif command == 'echo':
            output = self.commands.echo(args)
        elif command == 'rev':
            output = self.commands.rev(args)
        elif command == 'exit':
            self.save_log()
            self.root.destroy()
            sys.exit(0)
        else:
            output = f"{command}: command not found"
        self.output_area.insert(END, output + '\n')

    def start_gui(self):
        self.root = tk.Tk()
        self.root.title('Shell Emulator')
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=24)
        self.output_area.pack()
        self.cmd_var = tk.StringVar()
        self.cmd_entry = tk.Entry(self.root, textvariable=self.cmd_var, width=80)
        self.cmd_entry.pack()
        self.cmd_entry.bind('<Return>', self.on_enter)
        self.update_prompt()

        if self.startup_script:
            self.run_startup_script()

        self.root.mainloop()

    def run_startup_script(self):
        try:
            with open(self.startup_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    self.output_area.insert(END, f"{self.prompt}{line}\n")
                    self.parse_command(line)
        except FileNotFoundError:
            self.output_area.insert(END, f"Startup script '{self.startup_script}' not found.\n")

    def on_enter(self, event):
        command_line = self.cmd_var.get()
        self.output_area.insert(END, f"{self.prompt}{command_line}\n")
        self.parse_command(command_line)
        self.cmd_var.set('')
        self.update_prompt()

    def update_prompt(self):
        self.prompt = f"{self.computer_name}:{self.current_path}$ "

def parse_args():
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('--computer_name', required=True, help='Computer name for the prompt')
    parser.add_argument('--vfs_path', required=True, help='Path to the virtual filesystem zip archive')
    parser.add_argument('--log_path', required=True, help='Path to the log file (JSON format)')
    parser.add_argument('--startup_script', help='Path to the startup script')
    return parser.parse_args()

def main():
    args = parse_args()
    emulator = ShellEmulator(args.computer_name, args.vfs_path, args.log_path, args.startup_script)
    emulator.start_gui()

if __name__ == '__main__':
    main()