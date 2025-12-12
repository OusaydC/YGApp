# DigitalOcean Deployment Guide
## Morocco Yield Gap Web Application

This guide will walk you through deploying your Django application to DigitalOcean and making it accessible online.

---

## 📋 Prerequisites

1. **DigitalOcean Account**: Sign up at [digitalocean.com](https://www.digitalocean.com)
2. **Domain Name** (optional but recommended): Purchase from Namecheap, GoDaddy, etc.
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)
4. **SSH Key**: Generate an SSH key pair for secure server access

---

## 🚀 Step 1: Prepare Your Application for Production

### 1.1 Update Django Settings for Production

Create a production settings file or update your existing `settings.py`:

**Key changes needed:**
- Set `DEBUG = False`
- Add your domain to `ALLOWED_HOSTS`
- Use environment variables for sensitive data (SECRET_KEY)
- Configure static files properly
- Set up proper database (PostgreSQL recommended for production)

### 1.2 Create `.env` file for environment variables

Create a `.env` file (and add it to `.gitignore`):
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 1.3 Update requirements.txt

Ensure all production dependencies are included (already done - gunicorn and whitenoise are present).

---

## 💻 Step 2: Create a DigitalOcean Droplet

1. **Log in** to DigitalOcean dashboard
2. Click **"Create"** → **"Droplets"**
3. **Choose configuration:**
   - **Image**: Ubuntu 22.04 LTS (recommended)
   - **Plan**: 
     - **Basic**: $6/month (1GB RAM) - Good for testing
     - **Basic**: $12/month (2GB RAM) - Recommended for production
     - **Basic**: $18/month (4GB RAM) - For higher traffic
   - **Datacenter**: Choose closest to your users
   - **Authentication**: 
     - **SSH keys** (recommended) - Add your public SSH key
     - OR **Password** - Set a root password
   - **Hostname**: e.g., `yieldgap-webapp`
4. Click **"Create Droplet"**

**Wait 1-2 minutes** for the droplet to be created.

---

## 🔐 Step 3: Connect to Your Server

### On Windows (PowerShell or Git Bash):

```bash
ssh root@YOUR_DROPLET_IP
```

Replace `YOUR_DROPLET_IP` with the IP address shown in your DigitalOcean dashboard.

**First time connection**: Type `yes` when prompted about authenticity.

---

## 🛠️ Step 4: Initial Server Setup

Once connected, run these commands:

### 4.1 Update System Packages

```bash
apt update && apt upgrade -y
```

### 4.2 Create a Non-Root User (Recommended)

```bash
adduser webapp
usermod -aG sudo webapp
su - webapp
```

### 4.3 Install Required Software

```bash
sudo apt install -y python3-pip python3-venv python3-dev postgresql postgresql-contrib nginx git curl
```

### 4.4 Install PostgreSQL

```bash
sudo -u postgres psql
```

In PostgreSQL prompt:
```sql
CREATE DATABASE yieldgap_db;
CREATE USER yieldgap_user WITH PASSWORD 'your_secure_password_here';
ALTER ROLE yieldgap_user SET client_encoding TO 'utf8';
ALTER ROLE yieldgap_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE yieldgap_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE yieldgap_db TO yieldgap_user;
\q
```

---

## 📦 Step 5: Deploy Your Application

### 5.1 Clone Your Repository

```bash
cd /home/webapp
git clone https://github.com/yourusername/your-repo.git
cd your-repo/WebAppYG
```

**OR** if you need to upload files manually:
```bash
# On your local machine, use SCP or SFTP
scp -r WebAppYG root@YOUR_DROPLET_IP:/home/webapp/
```

### 5.2 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If you have issues with GeoDjango dependencies, you may need:
```bash
sudo apt install -y binutils libproj-dev gdal-bin libgdal-dev
pip install GDAL==$(gdal-config --version)
```

### 5.4 Configure Environment Variables

```bash
nano .env
```

Add:
```
SECRET_KEY=generate-a-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,YOUR_DROPLET_IP
DATABASE_URL=postgresql://yieldgap_user:your_secure_password_here@localhost/yieldgap_db
```

**Generate a new SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5.5 Update Django Settings

Edit `yg_ma/settings.py`:

```python
import os
from decouple import config

# Security settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='yieldgap_db'),
        'USER': config('DB_USER', default='yieldgap_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (if you have uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Remove or comment out GeoDjango paths (they're Windows-specific)
# GEOS_LIBRARY_PATH = ...
# GDAL_LIBRARY_PATH = ...
# PROJ_LIB = ...
```

### 5.6 Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Create admin user
```

### 5.7 Load Your Data

```bash
python manage.py load_shapefiles
python manage.py load_variety_shapefiles
python manage.py load_real_data
```

---

## 🌐 Step 6: Configure Gunicorn

### 6.1 Test Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 yg_ma.wsgi:application
```

Visit `http://YOUR_DROPLET_IP:8000` in your browser. If it works, press `Ctrl+C` to stop.

### 6.2 Create Gunicorn Service

```bash
sudo nano /etc/systemd/system/yieldgap.service
```

Add:
```ini
[Unit]
Description=Gunicorn instance to serve Yield Gap Web App
After=network.target

[Service]
User=webapp
Group=www-data
WorkingDirectory=/home/webapp/your-repo/WebAppYG
Environment="PATH=/home/webapp/your-repo/WebAppYG/venv/bin"
ExecStart=/home/webapp/your-repo/WebAppYG/venv/bin/gunicorn --workers 3 --bind unix:/home/webapp/your-repo/WebAppYG/yieldgap.sock yg_ma.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Update paths** to match your actual directory structure.

### 6.3 Start and Enable Service

```bash
sudo systemctl start yieldgap
sudo systemctl enable yieldgap
sudo systemctl status yieldgap
```

---

## 🔧 Step 7: Configure Nginx

### 7.1 Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/yieldgap
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com YOUR_DROPLET_IP;

    location /static/ {
        alias /home/webapp/your-repo/WebAppYG/staticfiles/;
    }

    location /media/ {
        alias /home/webapp/your-repo/WebAppYG/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/webapp/your-repo/WebAppYG/yieldgap.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Update paths** to match your directory structure.

### 7.2 Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/yieldgap /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### 7.3 Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

---

## 🔒 Step 8: Set Up SSL with Let's Encrypt (HTTPS)

### 8.1 Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2 Get SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts. Certbot will automatically configure Nginx for HTTPS.

### 8.3 Auto-Renewal

Certbot sets up auto-renewal automatically. Test it:
```bash
sudo certbot renew --dry-run
```

---

## 🌍 Step 9: Configure Domain Name (Optional)

1. **In your domain registrar** (Namecheap, GoDaddy, etc.):
   - Go to DNS settings
   - Add an **A Record**:
     - **Host**: `@` or leave blank
     - **Value**: Your DigitalOcean droplet IP
     - **TTL**: 3600 (or default)
   - Add another **A Record** for `www`:
     - **Host**: `www`
     - **Value**: Your DigitalOcean droplet IP

2. **Wait 5-60 minutes** for DNS propagation

3. **Update ALLOWED_HOSTS** in your `.env` file:
   ```
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

4. **Restart services**:
   ```bash
   sudo systemctl restart yieldgap
   sudo systemctl restart nginx
   ```

---

## ✅ Step 10: Verify Deployment

1. Visit `http://YOUR_DROPLET_IP` or `https://yourdomain.com`
2. Check that the map loads correctly
3. Test all features
4. Check logs if issues:
   ```bash
   sudo journalctl -u yieldgap -f
   sudo tail -f /var/log/nginx/error.log
   ```

---

## 🔄 Step 11: Set Up Automatic Deployments (Optional)

### Using Git Hooks:

1. Create a deployment script:
```bash
nano /home/webapp/deploy.sh
```

```bash
#!/bin/bash
cd /home/webapp/your-repo/WebAppYG
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart yieldgap
```

2. Make it executable:
```bash
chmod +x /home/webapp/deploy.sh
```

3. Set up a webhook in your Git repository to call this script.

---

## 📊 Monitoring & Maintenance

### View Application Logs

```bash
sudo journalctl -u yieldgap -f
```

### View Nginx Logs

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
sudo systemctl restart yieldgap
sudo systemctl restart nginx
```

### Update Application

```bash
cd /home/webapp/your-repo/WebAppYG
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart yieldgap
```

---

## 🐛 Troubleshooting

### Application not loading?
- Check Gunicorn: `sudo systemctl status yieldgap`
- Check Nginx: `sudo systemctl status nginx`
- Check logs: `sudo journalctl -u yieldgap -n 50`

### Static files not loading?
- Run: `python manage.py collectstatic --noinput`
- Check Nginx static file path in config
- Check file permissions: `sudo chown -R webapp:www-data /home/webapp/your-repo/WebAppYG/staticfiles`

### Database connection errors?
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database credentials in `.env`
- Check database exists: `sudo -u postgres psql -l`

### Permission errors?
```bash
sudo chown -R webapp:www-data /home/webapp/your-repo
sudo chmod -R 755 /home/webapp/your-repo
```

---

## 💰 Estimated Costs

- **Droplet**: $6-18/month (depending on plan)
- **Domain**: $10-15/year (optional)
- **Total**: ~$6-20/month

---

## 📚 Additional Resources

- [DigitalOcean Django Tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## 🎉 Success!

Your website should now be live at `https://yourdomain.com` or `http://YOUR_DROPLET_IP`!

For any issues, check the logs and ensure all services are running.

