# Fixing Upload Issues Behind Nginx

## Common Issues and Solutions

### 1. File Size Limits

**Problem**: Uploads fail silently or return 413 errors.

**Solution**: Ensure both nginx and Flask allow large enough files:

- **Nginx**: Set `client_max_body_size` in the server block (not location block)
- **Flask**: Increase `MAX_CONTENT_LENGTH` in config.py

### 2. Proxy Timeouts

**Problem**: Large uploads timeout before completing.

**Solution**: Increase proxy timeouts in nginx:

```nginx
proxy_connect_timeout 300s;
proxy_send_timeout 300s;
proxy_read_timeout 300s;
```

### 3. Buffering Issues

**Problem**: Uploads hang or fail for large files.

**Solution**: Disable buffering for uploads:

```nginx
proxy_buffering off;
proxy_request_buffering off;
client_body_buffer_size 128k;
```

### 4. Volume Mount Conflicts

**Problem**: Files upload but aren't accessible or persist.

**Check docker-compose.yml**: You have both:
- Bind mount: `./:/app` (maps entire directory)
- Named volume: `uploads:/app/app/static/uploads` (conflicts!)

**Solution**: The named volume takes precedence. Files should persist in the Docker volume, but if you need them on the host, you can:

1. Remove the named volume and use only bind mount
2. Or keep the named volume and access files via Docker commands

### 5. Permissions Issues

**Problem**: Files fail to save due to permissions.

**Solution**: Ensure the upload directory is writable:

```bash
docker exec digital_signage_app mkdir -p /app/app/static/uploads
docker exec digital_signage_app chown -R $(docker exec digital_signage_app id -u):$(docker exec digital_signage_app id -g) /app/app/static/uploads
docker exec digital_signage_app chmod -R 755 /app/app/static/uploads
```

## Quick Fix Checklist

1. ✅ Update `app/config.py` - `MAX_CONTENT_LENGTH = 10 * 1024 * 1024` (10MB)
2. ✅ Update nginx config with increased timeouts and disabled buffering
3. ✅ Ensure `client_max_body_size 10M` is in the server block
4. ✅ Check Docker volume permissions
5. ✅ Restart nginx: `sudo systemctl reload nginx`
6. ✅ Restart Docker containers: `docker compose restart app`

## Testing Uploads

After applying fixes:

1. Check nginx error logs:
   ```bash
   sudo tail -f /var/log/nginx/digital-signage-error.log
   ```

2. Check Docker logs:
   ```bash
   docker logs -f digital_signage_app
   ```

3. Test with a small image first (< 1MB)
4. Then test with a larger image (2-5MB)

## Diagnostic Commands

Run the diagnostic script:
```bash
sudo ./nginx/diagnose-uploads.sh
```

Check upload directory:
```bash
docker exec digital_signage_app ls -la /app/app/static/uploads/
```

Check disk space:
```bash
df -h
docker system df
```

