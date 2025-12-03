#!/bin/bash

# Nginx Reverse Proxy Setup Script with Let's Encrypt SSL
# This script sets up nginx as a reverse proxy for the Digital Signage App
# with SSL certificates from Let's Encrypt

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Get domain name
echo ""
print_info "Nginx Reverse Proxy Setup for Digital Signage App"
echo ""
read -p "Enter your domain name (e.g., signage.example.com): " DOMAIN_NAME

if [ -z "$DOMAIN_NAME" ]; then
    print_error "Domain name is required"
    exit 1
fi

# Get email for Let's Encrypt
read -p "Enter your email for Let's Encrypt notifications: " EMAIL

if [ -z "$EMAIL" ]; then
    print_error "Email is required for Let's Encrypt"
    exit 1
fi

# Validate email format (basic check)
if [[ ! "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    print_error "Invalid email format"
    exit 1
fi

print_info "Setting up nginx reverse proxy for domain: $DOMAIN_NAME"

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    OS_VERSION=$VERSION_ID
else
    print_error "Cannot detect OS. This script supports Ubuntu/Debian."
    exit 1
fi

print_info "Detected OS: $OS $OS_VERSION"

# Install nginx and certbot
print_info "Installing nginx and certbot..."

if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    apt-get update
    apt-get install -y nginx certbot python3-certbot-nginx
    
    # Start and enable nginx
    systemctl enable nginx
    systemctl start nginx
else
    print_error "Unsupported OS. Please install nginx and certbot manually."
    exit 1
fi

# Create certbot webroot directory
print_info "Creating certbot webroot directory..."
mkdir -p /var/www/certbot
chown -R www-data:www-data /var/www/certbot

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check for existing configurations that might conflict
print_info "Checking for existing nginx configurations..."
EXISTING_SITES=$(ls /etc/nginx/sites-enabled/ 2>/dev/null | grep -v "digital-signage" || true)
if [ -n "$EXISTING_SITES" ]; then
    print_warn "Found existing nginx sites:"
    echo "$EXISTING_SITES" | while read site; do
        echo "  - $site"
    done
    print_warn "Multiple sites listening on port 443 may cause warnings"
    print_warn "Consider using 'default_server' or separate IP addresses"
fi

# Check for broken certificate references
print_info "Checking for broken certificate references..."
BROKEN_CERTS=$(grep -r "ssl_certificate" /etc/nginx/sites-enabled/ 2>/dev/null | grep -v "^#" | sed 's/.*ssl_certificate[^;]*\/\([^/]*\)\/.*/\1/' | sort -u || true)
if [ -n "$BROKEN_CERTS" ]; then
    for cert_domain in $BROKEN_CERTS; do
        if [ ! -f "/etc/letsencrypt/live/$cert_domain/fullchain.pem" ]; then
            print_warn "Warning: Site references missing certificate: $cert_domain"
            print_warn "  This may cause nginx test failures. Consider removing or fixing that site configuration."
        fi
    done
fi

# Generate nginx configuration
print_info "Generating nginx configuration..."
NGINX_CONF="/etc/nginx/sites-available/digital-signage"
sed "s/DOMAIN_NAME/$DOMAIN_NAME/g" "$SCRIPT_DIR/nginx.conf.template" > "$NGINX_CONF"

# Enable the site
print_info "Enabling nginx site..."
if [ -L /etc/nginx/sites-enabled/digital-signage ]; then
    rm /etc/nginx/sites-enabled/digital-signage
fi
ln -s /etc/nginx/sites-available/digital-signage /etc/nginx/sites-enabled/

# Remove default nginx site if it exists
if [ -L /etc/nginx/sites-enabled/default ]; then
    print_info "Removing default nginx site..."
    rm /etc/nginx/sites-enabled/default
fi

# Test nginx configuration
print_info "Testing nginx configuration..."
NGINX_TEST_OUTPUT=$(nginx -t 2>&1)
NGINX_TEST_EXIT=$?

if [ $NGINX_TEST_EXIT -eq 0 ]; then
    print_info "Nginx configuration is valid"
elif echo "$NGINX_TEST_OUTPUT" | grep -q "protocol options redefined"; then
    print_warn "Nginx test shows warnings about protocol options redefined"
    print_warn "This is usually harmless - multiple sites can listen on port 443"
    print_warn "However, if there are errors (not just warnings), please fix them first"
    if echo "$NGINX_TEST_OUTPUT" | grep -q "\\[emerg\\]"; then
        print_error "Nginx configuration has ERRORS (not just warnings):"
        echo "$NGINX_TEST_OUTPUT" | grep "\\[emerg\\]"
        print_error "Please fix the errors above before continuing"
        exit 1
    fi
    print_info "Only warnings detected, continuing..."
else
    print_error "Nginx configuration test failed:"
    echo "$NGINX_TEST_OUTPUT"
    exit 1
fi

# Reload nginx
print_info "Reloading nginx..."
systemctl reload nginx

# Obtain SSL certificate
print_info "Obtaining SSL certificate from Let's Encrypt..."
print_warn "Make sure your domain $DOMAIN_NAME points to this server's IP address"
read -p "Press Enter to continue with certificate generation..."

# Run certbot
if certbot --nginx -d "$DOMAIN_NAME" --non-interactive --agree-tos --email "$EMAIL" --redirect; then
    print_info "SSL certificate obtained successfully!"
else
    print_error "Failed to obtain SSL certificate"
    print_warn "You may need to:"
    print_warn "1. Ensure DNS is pointing to this server"
    print_warn "2. Ensure port 80 is open and accessible"
    print_warn "3. Run certbot manually: certbot --nginx -d $DOMAIN_NAME"
    exit 1
fi

# Set up automatic renewal
print_info "Setting up automatic certificate renewal..."
# Certbot automatically sets up a systemd timer, but we can verify it
if systemctl list-timers | grep -q certbot; then
    print_info "Certbot renewal timer is active"
else
    print_warn "Certbot renewal timer not found. Setting up manually..."
    systemctl enable certbot.timer
    systemctl start certbot.timer
fi

# Test renewal (dry run)
print_info "Testing certificate renewal (dry run)..."
if certbot renew --dry-run; then
    print_info "Certificate renewal test successful"
else
    print_warn "Certificate renewal test failed, but this may be normal"
fi

# Final nginx reload
print_info "Performing final nginx reload..."
systemctl reload nginx

# Summary
echo ""
print_info "=========================================="
print_info "Setup Complete!"
print_info "=========================================="
echo ""
print_info "Your site should now be accessible at:"
print_info "  https://$DOMAIN_NAME"
echo ""
print_info "Nginx configuration: $NGINX_CONF"
print_info "SSL certificate location: /etc/letsencrypt/live/$DOMAIN_NAME/"
echo ""
print_warn "Make sure your Flask app is running on port 8000"
print_warn "If using Docker, ensure the app container is running:"
print_warn "  docker compose up -d"
echo ""
print_info "Useful commands:"
print_info "  sudo systemctl status nginx    # Check nginx status"
print_info "  sudo nginx -t                  # Test nginx config"
print_info "  sudo systemctl reload nginx    # Reload nginx"
print_info "  sudo certbot renew            # Renew certificates manually"
print_info "  sudo certbot certificates      # List certificates"
echo ""

