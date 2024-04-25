import sys
import json
import radare
from langchain.chat_models.gigachat import GigaChat
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage

PROMT = """\
Ты бот, помогающий начинающим специалистам по компьютерной безопасности декомпилировать \
исполняемые файлы. Используй разметку markdown, по возможности переводи код на python. \
Пользователь прикрепил исполняемый файл.

Ты обязан следующие комманды, чтобы помочь пользователю:
- `/list_functions` Для того, чтобы получить список функций.
- `/decompile [funcname]` Чтобы получить декомпилированный код функции на C++.

Каждую комманду следует писать с новой строки. Пользователь не может вводить эти \
комманды, их должен вводить ты. Пользователь не видит вывод этих комманд, ты должен \
переписать вывод в понятном для новичка виде.

Например:
USER: Выведи код функции main
BOT: /decompile main
USER: Выведи все функции
BOT: /list_functions
"""


def answer(chat, messages, decompiler):
    output = ""
    used = False
    res = chat(messages)
    messages.append(res)
    for line in res.content.split("\n"):
        if line.startswith("`/"):
            line = line[1:-1]
        if line.startswith("/"):
            cmd_res = decompiler.command(line)
            messages.append(HumanMessage("ВЫВОД:\n" + cmd_res))
            used = True
        else:
            output += line + "\n"
    if used:
        output += answer(chat, messages, decompiler)
    return output.strip()


def main():
    chat = GigaChat()
    promt = SystemMessage(content=PROMT)
    messages = None
    decompiler = radare.Radare()
    while True:
        input_messages, filename = json.loads(input())
        decompiler.update(filename)
        if len(input_messages) == 1:
            messages = [promt]
        messages.append(HumanMessage(input_messages[-1]))
        print(json.dumps(answer(chat, messages, decompiler)))

    
if __name__ == "__main__":
    main()
