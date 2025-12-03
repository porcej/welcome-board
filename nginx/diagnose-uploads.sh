#!/bin/bash

# Diagnostic script for upload issues behind nginx

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

echo ""
print_info "Diagnosing upload issues..."
echo ""

# Check nginx config
NGINX_CONF="/etc/nginx/sites-available/digital-signage"
if [ -f "$NGINX_CONF" ]; then
    print_info "Checking nginx configuration..."
    
    # Check client_max_body_size
    if grep -q "client_max_body_size" "$NGINX_CONF"; then
        SIZE=$(grep "client_max_body_size" "$NGINX_CONF" | head -1 | awk '{print $2}' | sed 's/;//')
        print_info "  client_max_body_size: $SIZE"
    else
        print_warn "  client_max_body_size not found - default is 1M (may be too small)"
    fi
    
    # Check proxy timeouts
    if grep -q "proxy_read_timeout" "$NGINX_CONF"; then
        TIMEOUT=$(grep "proxy_read_timeout" "$NGINX_CONF" | head -1 | awk '{print $2}' | sed 's/;//')
        print_info "  proxy_read_timeout: $TIMEOUT"
    else
        print_warn "  proxy_read_timeout not found - default is 60s (may be too short for large uploads)"
    fi
    
    # Check if client_max_body_size is in the right location
    if grep -A 10 "location / {" "$NGINX_CONF" | grep -q "client_max_body_size"; then
        print_warn "  client_max_body_size is inside location block - should be in server block"
    fi
else
    print_error "Nginx config not found: $NGINX_CONF"
fi

# Check Docker container
print_info ""
print_info "Checking Docker container..."
if docker ps | grep -q digital_signage_app; then
    print_info "  Container is running"
    
    # Check upload folder exists
    if docker exec digital_signage_app test -d /app/app/static/uploads; then
        print_info "  Upload folder exists: /app/app/static/uploads"
        
        # Check permissions
        PERMS=$(docker exec digital_signage_app ls -ld /app/app/static/uploads | awk '{print $1, $3, $4}')
        print_info "  Upload folder permissions: $PERMS"
    else
        print_error "  Upload folder does not exist: /app/app/static/uploads"
    fi
    
    # Check volume mounts
    print_info "  Checking volume mounts..."
    docker inspect digital_signage_app --format '{{range .Mounts}}{{.Type}} {{.Destination}} -> {{.Source}}{{"\n"}}{{end}}' | grep uploads
    
else
    print_warn "  Container 'digital_signage_app' is not running"
fi

# Check nginx error logs
print_info ""
print_info "Recent nginx error log entries (last 10 lines):"
if [ -f "/var/log/nginx/digital-signage-error.log" ]; then
    tail -10 /var/log/nginx/digital-signage-error.log 2>/dev/null || echo "  (log file empty or not readable)"
else
    print_warn "  Error log not found: /var/log/nginx/digital-signage-error.log"
fi

echo ""
print_info "Common issues to check:"
echo "  1. client_max_body_size too small (should be at least 10M)"
echo "  2. Proxy timeouts too short for large files"
echo "  3. Volume mount conflicts between bind mount and named volume"
echo "  4. Permissions on upload directory"
echo "  5. Disk space on the server"
echo ""

