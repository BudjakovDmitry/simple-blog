# Simple blog engine

## Setup clean Debian 13 server

### Install pre-requirements

Login as root

```bash
su -
```

Update packages

```bash
apt update
apt upgrade
```

Install building tools

```bash
apt install build-essential gcc make
```

Install pre-requirements

```bash
apt install \
    wget \
    unzip \
    zlib1g-dev \
    gdb \
    lzma \
    lcov \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    libreadline-dev \
    libncurses5-dev \
    uuid-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    tk-dev \
    libzstd-dev \
    inetutils-inetd
```

### Build Python from source

Download Python

```bash
wget https://www.python.org/ftp/python/3.14.3/Python-3.14.3.tar.xz
```

Unpack

```bash
tar xvf Python-3.14.3.tar.xz
cd Python-3.14.3
```

Build

```bash
mkdir -p /opt/python/3.14.3
./configure --enable-optimizations --prefix=/opt/python/3.14.3
make -j$(nproc)
make altinstall
rm -r Python-3.14.3
```

Make symlink to PATH-dir

```bash
ln -s /opt/python/3.14.4/bin/python-3.14 /usr/local/bin/python
```

Upgrade pip

```bash
python -m pip instal -U pip
```

