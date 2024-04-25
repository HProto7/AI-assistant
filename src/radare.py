import os
import time
import subprocess


class Radare:
    def __init__(self):
        self.filename = None
        self.functions = None
        self.pipe_r, self.pipe_w = os.pipe()

    def execute(self, cmd):
        self.process.stdin.write((cmd + ";\n").encode())
        self.process.stdin.flush()
        time.sleep(0.1)
        output = ""
        while True:
            data = os.read(self.pipe_r, 4096)
            output += data.decode()
            if output.endswith("]> \033[0m"):
                break
        output = output.split("\n")[:-1]
        if output and output[0].startswith("\033"):
            output.pop(0)
        return "\n".join(output)

    def update(self, filename):
        if filename == self.filename:
            return
        self.filename = filename
        self.process = subprocess.Popen(
            ["r2", filename],
            stdin=subprocess.PIPE,
            stdout=self.pipe_w,
            stderr=subprocess.PIPE,
        )
        # Disable colored output
        self.execute("e scr.color = 0")
        # Analyze
        self.execute("aaa")

    def command(self, input_string):
        if self.filename is None:
            return "ОШИБКА: Файл не загружен"
        assert input_string.startswith("/")
        cmd, *args = input_string[1:].split()
        output = None
        match cmd:
            case "list_functions":
                return "```\n" + self.execute("afl") + "\n```"
            case "decompile":
                self.execute(f"s sym.{args[0]}")
                return "```c++\n" + self.execute("pdg") + "\n```"
