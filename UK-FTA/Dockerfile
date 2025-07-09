# For more information, please refer to https://aka.ms/vscode-docker-python
# Debian based
FROM python:3-slim-bookworm

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# Get prerequistes ------------------------------------------------------------------------
RUN apt update && apt install -y wget unzip tar ffmpeg

# ffmpeg & https://mkvtoolnix.download/downloads.html#debian
RUN wget -O /etc/apt/keyrings/gpg-pub-moritzbunkus.gpg https://mkvtoolnix.download/gpg-pub-moritzbunkus.gpg
RUN apt update && apt install -y mkvtoolnix mkvtoolnix-gui

# Bento 4 https://www.bento4.com/downloads/
RUN wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip
RUN unzip Bento4-SDK-*.zip  -d /tmp/bento4
RUN mkdir /usr/local/bento4
RUN cp -r /tmp/bento4/*/* /usr/local/bento4/
RUN rm -rf /tmp/bento4
RUN rm Bento4-SDK-*.zip

# https://github.com/nilaoda/N_m3u8DL-RE/releases
RUN wget https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.3.0-beta/N_m3u8DL-RE_v0.3.0-beta_linux-x64_20241203.tar.gz
RUN tar -zxvf N_m3u8DL-RE_*.tar.gz N_m3u8DL-RE
RUN mv N_m3u8DL-RE /usr/local/bin/

# https://github.com/shaka-project/shaka-packager/releases
RUN wget https://github.com/shaka-project/shaka-packager/releases/download/v3.4.2/packager-linux-x64
RUN chmod +x packager-linux-x64
RUN mv packager-linux-x64 /usr/local/bin/shaka-packager

ENV PATH="$PATH:/usr/local/bento4/bin"
 
RUN apt install -y build-essential
RUN pip3 install --upgrade pip setuptools wheel Cython

# Install pip requirements ----------------------------------------------------------------
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Mount /save from host
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# 5678
#ARG APP_UID
#ARG APP_USER
#RUN adduser -u ${APP_UID} --disabled-password --gecos "" ${APP_USER} && chown -R ${APP_USER} /app
RUN mkdir /save 
#&& chown -R ${APP_USER} /save
#USER ${APP_USER}


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python", "itvx.py"]
CMD ["--help"]
