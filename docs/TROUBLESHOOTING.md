# Troubleshooting Guide

This guide helps resolve common issues when setting up and using the Qlik MCP Server.

## Connection Issues

### Certificate Errors

**Error**: `SSL certificate verify failed`

**Solutions**:
1. Verify `root.pem` matches your Qlik server's certificate
2. Check that server URL matches certificate CN/SAN
3. Ensure certificates are in PEM format (not DER/P12)
4. Verify certificate files are readable (`chmod 644 certs/*.pem`)

**Error**: `SSL handshake failed`

**Solutions**:
1. Ensure `client.pem` and `client_key.pem` are a matching pair
2. Check that certificates haven't expired
3. Verify certificate files exist and are not empty

### Authentication Issues

**Error**: `Access denied` or `Authentication failed`

**Solutions**:
1. Check `QLIK_USER_DIRECTORY` and `QLIK_USER_ID` in `.env`
2. Verify the client certificate has Engine API access in QMC
3. Ensure the user exists in the specified directory
4. Check if the certificate is associated with the correct user

### Connection Timeouts

**Error**: `Connection timeout` or `WebSocket connection failed`

**Solutions**:
1. Verify `QLIK_SERVER_URL` and `QLIK_SERVER_PORT` are correct
2. Check network connectivity to Qlik server
3. Ensure firewall allows connections on port 4747
4. Increase timeout in `.env`: `QLIK_TIMEOUT=60000`

### Application Access Issues

**Error**: `App not found` or `Access denied to app`

**Solutions**:
1. Verify the application ID is correct
2. Check user has access to the app in QMC
3. Ensure the app is published if using a service account
4. Verify the app exists and isn't in a restricted stream

## MCP Server Issues

### Server Won't Start

**Error**: `No module named 'fastmcp'`

**Solutions**:
1. Ensure Python 3.10+ is installed
2. Install dependencies: `pip install -r requirements.txt`
3. Use correct Python version: `/opt/homebrew/bin/python3.11`

**Error**: `Port already in use`

**Solutions**:
1. Check if another MCP server is running
2. Kill existing processes: `pkill -f "src.server"`
3. Use a different port in server configuration

### Claude Desktop Integration

**Error**: `Tool not found` in Claude Desktop

**Solutions**:
1. Restart Claude Desktop after configuration changes
2. Verify `claude_desktop_config.json` syntax is correct
3. Check file paths in configuration are absolute and correct
4. Ensure `.env` file is configured properly

**Error**: `Server connection failed`

**Solutions**:
1. Check server logs for errors
2. Verify the server starts successfully: `python -m src.server`
3. Test individual tools with test scripts
4. Check Python path and environment variables

## Tool-Specific Issues

### Empty Results

**Error**: Tools return empty arrays or no data

**Solutions**:
1. Verify the application contains the requested objects
2. Check user permissions for the specific app
3. Test with a known application ID
4. Review application logs in QMC

### Slow Performance

**Error**: Tools take a long time to respond

**Solutions**:
1. Large applications may take time to process
2. Consider filtering options to reduce data
3. Check Qlik server performance and load
4. Verify network latency to Qlik server

## Testing and Diagnostics

### Running Diagnostics

Test basic connectivity:
```bash
# Test Qlik connection
python tests/test_qlik_connection.py

# Test application listing (should work if connection is good)
python tests/test_list_apps.py

# Test specific tool functionality
python tests/test_measures.py
```

### Enable Debug Logging

Add to your `.env` file:
```env
DEBUG=true
```

This will provide detailed logging for troubleshooting.

### Verify Certificate Chain

Test certificate files manually:
```bash
# Verify certificate format
openssl x509 -in certs/client.pem -text -noout

# Check certificate expiration
openssl x509 -in certs/client.pem -noout -dates

# Verify private key matches certificate
openssl x509 -noout -modulus -in certs/client.pem | openssl md5
openssl rsa -noout -modulus -in certs/client_key.pem | openssl md5
```

The MD5 hashes should match if the certificate and key are a pair.

## Environment Configuration Issues

### Missing Environment Variables

**Error**: `Environment variable not found`

**Solutions**:
1. Copy `.env.example` to `.env`
2. Fill in all required variables
3. Verify `.env` file is in project root
4. Check for typos in variable names

### Incorrect Paths

**Error**: `File not found` for certificates

**Solutions**:
1. Use paths relative to project root
2. Verify certificate files exist at specified paths
3. Check file permissions and ownership
4. Use absolute paths if relative paths fail

## Getting Help

If you continue to experience issues:

1. **Check the logs**: Enable debug logging and review output
2. **Test incrementally**: Use individual test scripts to isolate issues
3. **Verify prerequisites**: Ensure all requirements are met
4. **Review configuration**: Double-check all paths and settings
5. **Test certificates**: Verify certificate setup independently

### Common Resolution Steps

1. **Restart everything**:
   ```bash
   # Kill any running servers
   pkill -f "src.server"
   
   # Restart Claude Desktop
   # Restart the MCP server
   python -m src.server
   ```

2. **Verify complete setup**:
   ```bash
   # Check Python version
   python --version
   
   # Verify dependencies
   pip list | grep fastmcp
   
   # Test basic connection
   python tests/test_qlik_connection.py
   ```

3. **Clean restart**:
   ```bash
   # Remove any cached files
   find . -name "__pycache__" -exec rm -rf {} +
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```