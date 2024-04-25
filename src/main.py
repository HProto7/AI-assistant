import json
import subprocess
import gradio as gr


class Chat:
    def __init__(self):
        self.process = subprocess.Popen(
            ["sh", "-c", ". .venv/bin/activate && python src/chat.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def send(self, data):
        self.process.stdin.write((json.dumps(data) + "\n").encode())
        self.process.stdin.flush()
        return json.loads(self.process.stdout.readline())


def get_response(message, history, filename):
    return get_response.chat.send([history + [message], filename])


def upload_file(filepath):
    subprocess.call["mv", filepath, "input"]


def main():
    get_response.chat = Chat()
    upload_btn = gr.UploadButton("Upload executable", render=False)
    gr.ChatInterface(
        fn=get_response,
        title="Gigampiler",
        additional_inputs=[upload_btn],
    ).launch()


if __name__ == "__main__":
    main()
