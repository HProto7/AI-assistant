FROM python:3.11
# Gradio
RUN pip install gradio
# GigaChain
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install gigachain && \
    pip install gigachain-cli && \
    gigachain install-rus-certs
# Radare2
RUN curl -Ls https://github.com/radareorg/radare2/releases/download/5.9.0/radare2-5.9.0.tar.xz \
    | tar xJv && \
    radare2-5.9.0/sys/install.sh && \
    r2pm -ci r2ghidra
# App
ENV GRADIO_SERVER_NAME="0.0.0.0"
COPY ./secret.sh ./secret.sh
COPY ./src ./src
EXPOSE 7860
CMD ["bash", "-c", "source ./secret.sh && python ./src/main.py"]
