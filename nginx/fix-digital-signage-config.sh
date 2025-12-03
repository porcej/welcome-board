#!/bin/bash

# Quick fix script to comment out the HTTPS server block if certificates don't exist yet

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

# Extract domain from the config
DOMAIN=$(grep "server_name" "$NGINX_CONF" | head -1 | awk '{print $2}' | sed 's/;//')

if [ -z "$DOMAIN" ]; then
    print_error "Could not determine domain from configuration"
    exit 1
fi

print_info "Checking certificate for domain: $DOMAIN"

CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"

if [ -f "$CERT_PATH" ]; then
    print_info "Certificate exists: $CERT_PATH"
    print_info "Configuration should be fine. If you're seeing errors, check for other issues."
    
    # Check if HTTPS server block is commented out
    if grep -q "^#server {" "$NGINX_CONF" && grep -q "listen 443" "$NGINX_CONF"; then
        print_warn "HTTPS server block appears to be commented out but certificate exists"
        print_warn "You may need to uncomment it or run: certbot --nginx -d $DOMAIN"
    fi
else
    print_warn "Certificate does not exist: $CERT_PATH"
    print_info "Checking if HTTPS server block needs to be commented out..."
    
    # Check if there's an uncommented HTTPS server block without certificates
    if grep -q "^[^#]*listen 443 ssl" "$NGINX_CONF"; then
        print_warn "Found uncommented HTTPS server block without certificate"
        print_info "The configuration should have the HTTPS block commented out initially"
        print_info "Run certbot to obtain the certificate: certbot --nginx -d $DOMAIN"
    fi
fi

# Test nginx configuration
print_info "Testing nginx configuration..."
if nginx -t 2>&1 | grep -q "\\[emerg\\]"; then
    print_error "Nginx configuration has errors:"
    nginx -t 2>&1 | grep "\\[emerg\\]"
    exit 1
else
    print_info "Nginx configuration test passed (warnings are OK)"
fi

