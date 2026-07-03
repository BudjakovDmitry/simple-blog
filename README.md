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
apt install postgresql wget curl unzip tree vim ca-certificates
```

Install building tools:

```bash
apt install build-essential gcc make
```

Install pre-requirements:

```bash
apt install \
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

### Install Angie web-server

Download Angie repository open key

```bash
curl -o /etc/apt/trusted.gpg.d/angie-signing.gpg https://angie.software/keys/angie-signing.gpg
```

Connect to the Angie repository

```bash
echo "deb https://download.angie.software/angie/$(. /etc/os-release && echo "$ID/$VERSION_ID $VERSION_CODENAME") main" \
     | tee /etc/apt/sources.list.d/angie.list > /dev/null
```

Update repository index

```bash
apt update
```

Install Angie

```bash
apt install angie
```

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

### Prepare database

Afrer installation, Postgres will create the `postgres` user. To connect to the DBMS, we need to log in to the operating system as this user. We can either set the `postgres` user's password: `passwd postgres` and then log in with the given password: `su - postgres`; or we can log in as the `root` user and then as the `postgres` user: `su - && su postgres`. In both cases, we need `root` privileges.

When we logged in as `postgres` we can connect to database using `psql`

```bash
su -
su postgres
psql
```

Create role

```sql
CREATE ROLE dmitbud WITH LOGIN PASSWORD 'MyStrongPassword';
```

Create database

```sql
CREATE DATABASE dmitbud
WITH
ENCODING='UTF8'
owner dmitbud;
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

Update secrets:

```bash
mv secrets/pgpass.example secrets/pgpass
chmod 600 secrets/pgpass
```

Set your own credentials to `secrets/pg_service.conf` and `pgpass`.

For production.

Make shared static directory

```bash
sudo mkdir -p /var/www/blog/static
sudo chown -R www:angie /var/www/blog
sudo find /var/www/blog/static -type d -exec chmod 750 {} \;
sudo find /var/www/blog/static -type f -exec chmod 640 {} \;
```

```bash
make collectstatic
sudo install -m 0644 deploy/angie/dmitbud.conf /etc/angie/http.d/dmitbud.conf
sudo mv /etc/angie/http.d/default.conf /etc/angie/http.d/default.conf.factory
sudo angie -t
# or
sudo /usr/sbin/angie -t
sudo systemctl reload angie
```

