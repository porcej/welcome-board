#!/bin/bash

# Script to fix redirect loop in nginx configuration
# The issue is having a server block listening on 443 that redirects to HTTPS

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root (use sudo)"
    exit 1
fi

NGINX_CONF="/etc/nginx/sites-available/digital-signage"

if [ ! -f "$NGINX_CONF" ]; then
    print_error "Configuration file not found: $NGINX_CONF"
    exit 1
fi

print_info "Analyzing nginx configuration for redirect loops..."

# Check if there's a server block on 443 that redirects
if grep -A 20 "listen 443" "$NGINX_CONF" | grep -q "return 301 https"; then
    print_warn "Found server block listening on 443 that redirects to HTTPS - this causes a loop!"
    print_info "Creating backup of current configuration..."
    cp "$NGINX_CONF" "${NGINX_CONF}.backup.$(date +%Y%m%d_%H%M%S)"
    
    print_info "Please manually edit the configuration to remove the problematic server block"
    print_info "Configuration file: $NGINX_CONF"
    echo ""
    print_warn "The configuration should have:"
    echo "  1. One HTTP server block (port 80) that redirects to HTTPS"
    echo "  2. One HTTPS server block (port 443) that proxies to the app"
    echo ""
    print_warn "Remove any server blocks on port 443 that redirect to HTTPS"
fi

print_info "Here's what needs to be fixed:"
echo ""
echo "The correct configuration should look like this:"
echo ""
echo "# HTTP server - redirects to HTTPS"
echo "server {"
echo "    listen 80;"
echo "    listen [::]:80;"
echo "    server_name hellobrd.com;"
echo "    location /.well-known/acme-challenge/ {"
echo "        root /var/www/certbot;"
echo "    }"
echo "    location / {"
echo "        return 301 https://\$host\$request_uri;"
echo "    }"
echo "}"
echo ""
echo "# HTTPS server - proxies to app"
echo "server {"
echo "    listen 443 ssl http2;"
echo "    listen [::]:443 ssl http2;"
echo "    server_name hellobrd.com;"
echo "    # SSL certs..."
echo "    location / {"
echo "        proxy_pass http://app_server;"
echo "        # proxy settings..."
echo "    }"
echo "}"
echo ""
