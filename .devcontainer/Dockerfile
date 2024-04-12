# This image has selenium and chrome driver already installed
FROM rofrano/pipeline-selenium:latest

# Set up the Python development environment
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN sudo python -m pip install --upgrade pip poetry && \
    sudo poetry config virtualenvs.create false && \
    sudo poetry install

# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp && bash ./install-tools.sh
