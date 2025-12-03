# Nginx Reverse Proxy Setup

This directory contains scripts and configuration files to set up nginx as a reverse proxy for the Digital Signage App with SSL certificates from Let's Encrypt.

## Prerequisites

1. **Domain Name**: You need a domain name pointing to your server's IP address
2. **Root Access**: The setup script requires root/sudo privileges
3. **Open Ports**: Ensure ports 80 (HTTP) and 443 (HTTPS) are open in your firewall
4. **DNS Configuration**: Your domain's A record should point to your server's public IP

## Quick Setup

1. Make the setup script executable:
   ```bash
   chmod +x nginx/setup-nginx.sh
   ```

2. Run the setup script:
   ```bash
   sudo ./nginx/setup-nginx.sh
   ```

3. Follow the prompts:
   - Enter your domain name (e.g., `signage.example.com`)
   - Enter your email address for Let's Encrypt notifications

4. Ensure your Flask app is running:
   ```bash
   docker compose up -d
   ```

## What the Script Does

1. **Installs nginx and certbot** (if not already installed)
2. **Creates nginx configuration** as a reverse proxy to your Flask app (port 8000)
3. **Obtains SSL certificate** from Let's Encrypt
4. **Configures automatic renewal** of SSL certificates
5. **Sets up HTTP to HTTPS redirect**

## Manual Setup (Alternative)

If you prefer to set up manually or the script doesn't work for your system:

### 1. Install nginx and certbot

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

**CentOS/RHEL:**
```bash
sudo yum install -y nginx certbot python3-certbot-nginx
```

### 2. Copy and customize nginx configuration

```bash
sudo cp nginx/nginx.conf.template /etc/nginx/sites-available/digital-signage
sudo sed -i "s/DOMAIN_NAME/your-domain.com/g" /etc/nginx/sites-available/digital-signage
```

### 3. Enable the site

```bash
sudo ln -s /etc/nginx/sites-available/digital-signage /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

### 4. Obtain SSL certificate

```bash
sudo certbot --nginx -d your-domain.com --non-interactive --agree-tos --email your-email@example.com --redirect
```

### 5. Verify automatic renewal

```bash
sudo certbot renew --dry-run
```

## Configuration Details

The nginx configuration:
- **Proxies to**: `http://127.0.0.1:8005` (your Flask app - matches docker-compose port mapping)
- **Note**: If your app runs on a different port, update the `upstream app_server` section in the nginx config
- **SSL**: Uses Let's Encrypt certificates
- **Security Headers**: Includes HSTS, X-Frame-Options, etc.
- **File Uploads**: Allows up to 10MB
- **Static Files**: Serves from `/app/app/static/` with caching

## Troubleshooting

### Nginx Test Fails with Certificate Errors

If you see errors like:
```
cannot load certificate "/etc/letsencrypt/live/domain.com/fullchain.pem": BIO_new_file() failed
```

This means a site configuration references a certificate that doesn't exist. To fix:

1. **Identify broken references**:
   ```bash
   sudo ./nginx/fix-broken-certs.sh
   ```

2. **Fix the broken site**:
   - Remove the site if no longer needed: `sudo rm /etc/nginx/sites-enabled/broken-site`
   - Or comment out the server block in the site file
   - Or obtain a new certificate: `sudo certbot --nginx -d domain.com`

### Protocol Options Redefined Warnings

If you see warnings like:
```
protocol options redefined for 0.0.0.0:443
```

This is usually harmless - multiple sites can listen on port 443. However, if you want to avoid the warning:

1. **Use default_server** (only for one site):
   ```nginx
   listen 443 ssl http2 default_server;
   ```

2. **Use separate IP addresses** for each site

3. **Use SNI** (Server Name Indication) - nginx handles this automatically

### Certificate Generation Fails

1. **Check DNS**: Ensure your domain points to the server
   ```bash
   dig your-domain.com
   ```

2. **Check Port 80**: Ensure it's open and accessible
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

3. **Check nginx**: Ensure nginx is running
   ```bash
   sudo systemctl status nginx
   ```

### App Not Accessible

1. **Check Flask app is running**:
   ```bash
   docker compose ps
   curl http://localhost:8000
   ```

2. **Check nginx logs**:
   ```bash
   sudo tail -f /var/log/nginx/digital-signage-error.log
   ```

3. **Test nginx configuration**:
   ```bash
   sudo nginx -t
   ```

### Certificate Renewal Issues

1. **Test renewal manually**:
   ```bash
   sudo certbot renew --dry-run
   ```

2. **Check certbot timer**:
   ```bash
   sudo systemctl status certbot.timer
   ```

3. **Manual renewal**:
   ```bash
   sudo certbot renew
   sudo systemctl reload nginx
   ```

## Firewall Configuration

If using UFW (Ubuntu):
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

If using firewalld (CentOS/RHEL):
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## Updating Configuration

After modifying the nginx configuration:

```bash
sudo nginx -t  # Test configuration
sudo systemctl reload nginx  # Reload without downtime
```

## Files

- `nginx.conf.template`: Nginx configuration template
- `setup-nginx.sh`: Automated setup script
- `README.md`: This file

## Notes

- The nginx configuration assumes your Flask app runs on port 8005 (matching docker-compose.yml)
- If your app runs on a different port, update the `upstream app_server` section in `nginx.conf.template`
- The port mapping in docker-compose.yml is `8005:8000` (host:container)
- SSL certificates are automatically renewed by certbot
- The configuration includes security headers and optimizations

