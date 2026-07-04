# Simple blog engine

## Setup clean Debian 13 server

### Install pre-requirements

Login as root:

```bash
su -
```

Update packages:

```bash
apt update && apt upgrade
```

Install utils:

```bash
apt install wget curl unzip tree vim
```

Install building tools:

```bash
apt install build-essential gcc make
```

Install pre-requirements:

```bash
apt install \
    ca-certificates \
    debian-archive-keyring \
    zlib1g-dev \
    gdb \
    gnupg2 \
    lzma \
    lcov \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    libreadline-dev \
    libncurses5-dev \
    lsb-release \
    uuid-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    tk-dev \
    libzstd-dev \
    inetutils-inetd
```

### Install Nginx

Import an official nginx signing key

```bash
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
```

Set up the apt repository for stable nginx packages:

```bash
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Set up repository pinning to prefer nginx packages over distribution-provided ones:

```bash
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx
```

Install Nginx

```bash
apt update && apt install nginx
```

### Install and prepare PostgreSQL

Install PostgreSQL

```bash
apt install postgresql
```

Login as a `postgres` user an use `psql` tool to connect to Postgres.

```bash
su - postgres
psql
```

Create role (don't forget to change password):

```sql
CREATE ROLE dmitbud WITH LOGIN PASSWORD 'MyStrongPassword';
```

Create database:

```sql
CREATE DATABASE knowladge_base
WITH
ENCODING='UTF8'
owner dmitbud;
```

Now quit from `psql`: `\q` and logout from `postgres` user: `exit`.

### Build Python from source

Download Python:

```bash
wget https://www.python.org/ftp/python/3.14.3/Python-3.14.3.tar.xz
```

Unpack:

```bash
tar xvf Python-3.14.3.tar.xz
cd Python-3.14.3
```

Build:

```bash
mkdir -p /opt/python/3.14.3
./configure --enable-optimizations --prefix=/opt/python/3.14.3
make -j$(nproc)
make altinstall
cd ..
rm -r Python-3.14.3
rm Python-3.14.3.tar.xz
```

Make symlink to PATH dir

```bash
ln -s /opt/python/3.14.3/bin/python3.14 /usr/local/bin/python
```

Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Run project

Login as a regular user. Create `code` direcotory

```bash
mkdir $HOME/code
```

Download the project

```bash
wget https://github.com/BudjakovDmitry/simple-blog/archive/refs/heads/main.zip
```

Unzip project to `code`

```bash
unzip main.zip -d $HOME/code
mv $HOME/code/simple-blog-engine-main/ $HOME/code/blog
rm main.zip
cd $HOME/code/blog
```

Create and activate virtual environment

```bash
python -m venv env
source env/bin/activate
```

Install project requirements

```bash
pip install --upgrade pip
python -m pip install -r requirements.txt
```

Set your own credentials to `secrets/pg_service.conf` and `pgpass`.

### For production

Login as a regular user.

Make shared static directories

```bash
# static files
sudo mkdir -p /var/dmitbud/static
# secrets
sudo mkdir -p /etc/dmitbud/postgres
# sudo chown -R www:angie /var/www/blog
# sudo find /var/www/blog/static -type d -exec chmod 750 {} \;
# sudo find /var/www/blog/static -type f -exec chmod 640 {} \;
```

Update secrets:

```bash
mv secrets/pgpass.example /etc/blog/postgres/pgpass
chmod 600 /etc/blog/postgres/pgpass
```

```bash
make collectstatic
sudo install -m 0644 deploy/angie/dmitbud.conf /etc/angie/http.d/dmitbud.conf
sudo mv /etc/angie/http.d/default.conf /etc/angie/http.d/default.conf.factory
sudo angie -t
# or
sudo /usr/sbin/angie -t
udo systemctl reload angie
```

