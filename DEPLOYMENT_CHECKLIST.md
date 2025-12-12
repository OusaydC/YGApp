# DigitalOcean Deployment Quick Checklist

Use this checklist to ensure you complete all steps for deploying your Django app to DigitalOcean.

## ✅ Pre-Deployment

- [ ] Code is committed to Git repository
- [ ] All dependencies are in `requirements.txt`
- [ ] `DEBUG = False` in production settings
- [ ] `ALLOWED_HOSTS` configured
- [ ] Secret key is not hardcoded (use environment variables)
- [ ] Static files configuration is correct
- [ ] Database migration files are up to date

## ✅ DigitalOcean Setup

- [ ] Created DigitalOcean account
- [ ] Created Ubuntu 22.04 LTS droplet ($6-18/month)
- [ ] Saved droplet IP address
- [ ] Added SSH key or set root password
- [ ] Can SSH into server: `ssh root@YOUR_IP`

## ✅ Server Initial Setup

- [ ] Updated system packages: `apt update && apt upgrade -y`
- [ ] Created non-root user: `adduser webapp`
- [ ] Installed Python, pip, venv: `apt install python3-pip python3-venv`
- [ ] Installed PostgreSQL: `apt install postgresql postgresql-contrib`
- [ ] Installed Nginx: `apt install nginx`
- [ ] Installed Git: `apt install git`

## ✅ Database Setup

- [ ] Created PostgreSQL database: `yieldgap_db`
- [ ] Created PostgreSQL user: `yieldgap_user`
- [ ] Set database password
- [ ] Granted privileges to user
- [ ] Tested database connection

## ✅ Application Deployment

- [ ] Cloned repository or uploaded files to server
- [ ] Created virtual environment: `python3 -m venv venv`
- [ ] Activated virtual environment: `source venv/bin/activate`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Created `.env` file with all environment variables
- [ ] Generated new SECRET_KEY
- [ ] Updated `settings.py` for production (or use `settings_production.py`)
- [ ] Ran migrations: `python manage.py migrate`
- [ ] Created superuser: `python manage.py createsuperuser`
- [ ] Collected static files: `python manage.py collectstatic --noinput`
- [ ] Loaded data: `python manage.py load_real_data`

## ✅ Gunicorn Setup

- [ ] Tested Gunicorn: `gunicorn --bind 0.0.0.0:8000 yg_ma.wsgi:application`
- [ ] Created systemd service file: `/etc/systemd/system/yieldgap.service`
- [ ] Started service: `sudo systemctl start yieldgap`
- [ ] Enabled service: `sudo systemctl enable yieldgap`
- [ ] Checked status: `sudo systemctl status yieldgap`

## ✅ Nginx Setup

- [ ] Created Nginx config: `/etc/nginx/sites-available/yieldgap`
- [ ] Created symlink: `ln -s /etc/nginx/sites-available/yieldgap /etc/nginx/sites-enabled/`
- [ ] Tested config: `sudo nginx -t`
- [ ] Restarted Nginx: `sudo systemctl restart nginx`
- [ ] Configured firewall: `sudo ufw allow 'Nginx Full'`

## ✅ SSL/HTTPS Setup

- [ ] Installed Certbot: `apt install certbot python3-certbot-nginx`
- [ ] Obtained SSL certificate: `sudo certbot --nginx -d yourdomain.com`
- [ ] Tested auto-renewal: `sudo certbot renew --dry-run`

## ✅ Domain Configuration (Optional)

- [ ] Purchased domain name
- [ ] Added A record pointing to droplet IP
- [ ] Added www A record pointing to droplet IP
- [ ] Updated `ALLOWED_HOSTS` in `.env` file
- [ ] Waited for DNS propagation (5-60 minutes)
- [ ] Restarted services after DNS update

## ✅ Verification

- [ ] Website loads at `http://YOUR_IP` or `https://yourdomain.com`
- [ ] Map displays correctly
- [ ] All features work (year selection, metric selection, etc.)
- [ ] Static files load (CSS, JS, images)
- [ ] Admin panel accessible at `/admin`
- [ ] No errors in logs: `sudo journalctl -u yieldgap -f`

## ✅ Security

- [ ] Firewall enabled: `sudo ufw status`
- [ ] Only necessary ports open (80, 443, 22)
- [ ] Strong database password set
- [ ] Strong SECRET_KEY generated
- [ ] DEBUG = False
- [ ] HTTPS working (SSL certificate installed)

## ✅ Monitoring & Maintenance

- [ ] Know how to view logs: `sudo journalctl -u yieldgap -f`
- [ ] Know how to restart services: `sudo systemctl restart yieldgap`
- [ ] Know how to update application (deployment script ready)
- [ ] Set up automated backups (optional but recommended)

---

## 🚨 Common Issues & Solutions

**Issue**: 502 Bad Gateway
- **Solution**: Check Gunicorn is running: `sudo systemctl status yieldgap`
- Check socket file path matches in both Gunicorn service and Nginx config

**Issue**: Static files not loading
- **Solution**: Run `python manage.py collectstatic --noinput`
- Check Nginx static file path is correct
- Check file permissions: `sudo chown -R webapp:www-data staticfiles/`

**Issue**: Database connection error
- **Solution**: Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database credentials in `.env`
- Check database exists: `sudo -u postgres psql -l`

**Issue**: Permission denied errors
- **Solution**: Fix ownership: `sudo chown -R webapp:www-data /home/webapp/your-repo`
- Fix permissions: `sudo chmod -R 755 /home/webapp/your-repo`

---

## 📞 Quick Commands Reference

```bash
# View application logs
sudo journalctl -u yieldgap -f

# Restart application
sudo systemctl restart yieldgap

# Restart Nginx
sudo systemctl restart nginx

# Check service status
sudo systemctl status yieldgap
sudo systemctl status nginx

# Update application
cd /home/webapp/your-repo/WebAppYG
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart yieldgap
```

---

**Need help?** Check the full `DEPLOYMENT_GUIDE.md` for detailed instructions.

