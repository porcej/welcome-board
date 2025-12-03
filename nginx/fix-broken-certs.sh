#!/bin/bash

# Script to identify and optionally fix broken certificate references in nginx

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

print_info "Scanning nginx configurations for broken certificate references..."

BROKEN_FOUND=0

# Check all enabled sites
for site_file in /etc/nginx/sites-enabled/*; do
    if [ -f "$site_file" ]; then
        site_name=$(basename "$site_file")
        
        # Extract certificate paths
        cert_paths=$(grep -h "ssl_certificate" "$site_file" 2>/dev/null | grep -v "^#" | grep -o "/etc/letsencrypt/live/[^/]*" | sort -u || true)
        
        for cert_path in $cert_paths; do
            domain=$(echo "$cert_path" | sed 's|/etc/letsencrypt/live/||')
            fullchain="$cert_path/fullchain.pem"
            
            if [ ! -f "$fullchain" ]; then
                BROKEN_FOUND=1
                print_warn "Broken certificate reference found:"
                echo "  Site: $site_name"
                echo "  Domain: $domain"
                echo "  Missing file: $fullchain"
                echo ""
            fi
        done
    fi
done

if [ $BROKEN_FOUND -eq 0 ]; then
    print_info "No broken certificate references found!"
    exit 0
fi

echo ""
print_warn "To fix these issues, you can:"
echo "  1. Remove the site configuration if it's no longer needed"
echo "  2. Comment out the server block in the site file"
echo "  3. Obtain a new certificate: certbot --nginx -d domain.com"
echo ""
read -p "Would you like to see which files contain these references? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Searching for certificate references..."
    grep -r "ssl_certificate" /etc/nginx/sites-enabled/ 2>/dev/null | grep -v "^#" || true
fi

