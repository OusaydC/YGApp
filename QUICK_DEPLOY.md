# Quick Deploy to DigitalOcean - Summary

## 🎯 The 5-Minute Overview

1. **Create Droplet** → Ubuntu 22.04, $6-18/month
2. **SSH into server** → `ssh root@YOUR_IP`
3. **Install software** → Python, PostgreSQL, Nginx
4. **Deploy app** → Clone repo, install deps, configure
5. **Set up web server** → Gunicorn + Nginx
6. **Add SSL** → Let's Encrypt (free HTTPS)
7. **Point domain** → DNS A record to your IP

**Total time**: 30-60 minutes  
**Cost**: $6-20/month

---

## 📝 Essential Commands

### On Your Server (SSH):

```bash
# 1. Update system
apt update && apt upgrade -y

# 2. Install required software
apt install -y python3-pip python3-venv postgresql nginx git

# 3. Set up database
sudo -u postgres psql
CREATE DATABASE yieldgap_db;
CREATE USER yieldgap_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE yieldgap_db TO yieldgap_user;
\q

# 4. Deploy application
cd /home/webapp
git clone YOUR_REPO_URL
cd WebAppYG
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment
nano .env
# Add: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DB credentials

# 6. Set up database
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 7. Test Gunicorn
gunicorn --bind 0.0.0.0:8000 yg_ma.wsgi:application
# Visit http://YOUR_IP:8000 - if it works, press Ctrl+C

# 8. Create Gunicorn service
sudo nano /etc/systemd/system/yieldgap.service
# (Copy config from DEPLOYMENT_GUIDE.md)

# 9. Start service
sudo systemctl start yieldgap
sudo systemctl enable yieldgap

# 10. Configure Nginx
sudo nano /etc/nginx/sites-available/yieldgap
# (Copy config from DEPLOYMENT_GUIDE.md)

# 11. Enable site
sudo ln -s /etc/nginx/sites-available/yieldgap /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 12. Set up SSL
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 🔑 Key Files to Create/Edit

### 1. `.env` file (in WebAppYG directory):
```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,YOUR_IP
DB_NAME=yieldgap_db
DB_USER=yieldgap_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Gunicorn Service (`/etc/systemd/system/yieldgap.service`):
```ini
[Unit]
Description=Gunicorn instance for Yield Gap Web App
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

### 3. Nginx Config (`/etc/nginx/sites-available/yieldgap`):
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com YOUR_IP;

    location /static/ {
        alias /home/webapp/your-repo/WebAppYG/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/webapp/your-repo/WebAppYG/yieldgap.sock;
    }
}
```

---

## ⚡ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| 502 Bad Gateway | `sudo systemctl restart yieldgap` |
| Static files 404 | `python manage.py collectstatic --noinput` |
| Can't connect | Check firewall: `sudo ufw status` |
| Database error | `sudo systemctl status postgresql` |

---

## 📚 Full Documentation

- **Detailed Guide**: See `DEPLOYMENT_GUIDE.md`
- **Checklist**: See `DEPLOYMENT_CHECKLIST.md`
- **Production Settings**: See `WebAppYG/yg_ma/settings_production.py`

---

## 🎉 After Deployment

Your site will be live at:
- `http://YOUR_DROPLET_IP` (immediately)
- `https://yourdomain.com` (after DNS + SSL setup)

**Monitor logs**: `sudo journalctl -u yieldgap -f`

