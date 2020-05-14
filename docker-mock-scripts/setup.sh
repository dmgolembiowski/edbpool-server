#!/bin/bash

cd /home/edbpool/edbpool \
    && /bin/bash docker-mock-scripts/phase_1/pyenv_installer.sh \
    && source ~/.bashrc \
    && pyenv install 3.8-dev \
    && pyenv shell 3.8-dev \
    && python3 -m venv . \
    && source bin/activate \
    && pip install -U pip wheel \
    && pip install -r dev-requirements.txt \
    && python3 docker-mock-scripts/phase_1/rpcserver.py "docker-mock-scripts/config.json"

