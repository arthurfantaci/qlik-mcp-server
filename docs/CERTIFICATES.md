# SSL Certificate Setup Guide

This guide explains how to obtain and configure the SSL certificates required to connect to Qlik Sense.

## Overview

The Qlik MCP Server uses certificate-based authentication to connect to the Qlik Sense Engine API. You need three certificate files:

- **Root Certificate** (`root.pem`) - Validates the Qlik server's identity
- **Client Certificate** (`client.pem`) - Identifies this client to Qlik Sense
- **Client Private Key** (`client_key.pem`) - Private key for the client certificate

## Obtaining Certificates

### Method 1: From Qlik Management Console (QMC)

1. **Access QMC**: Log into your Qlik Sense server's QMC (usually `https://your-server/qmc`)

2. **Navigate to Certificates**: Go to `Certificates` section in the QMC

3. **Export Certificates**: Click "Export certificates" and download the certificate bundle

4. **Extract Files**: The bundle typically contains:
   - `root.pem` (server root certificate)
   - `client.pem` (client certificate)
   - `client_key.pem` (client private key)

### Method 2: From Qlik Sense Server Directory

If you have access to the Qlik Sense server file system:

1. **Locate Certificate Directory**: Usually found at:
   ```
   C:\ProgramData\Qlik\Sense\Repository\Exported Certificates\.Local Certificates
   ```

2. **Copy Required Files**:
   - `root.pem`
   - `client.pem` 
   - `client_key.pem`

### Method 3: Request from Administrator

Contact your Qlik Sense administrator and request:
- Engine API access certificates
- Connection details (server URL, port, user directory, user ID)

## Certificate Installation

1. **Create Certificate Directory**:
   ```bash
   mkdir certs
   ```

2. **Place Certificate Files**:
   ```
   certs/
   ├── root.pem
   ├── client.pem
   └── client_key.pem
   ```

3. **Verify Permissions**: Ensure certificate files are readable:
   ```bash
   chmod 644 certs/*.pem
   ```

## Security Best Practices

- **Never commit certificates to version control** - They're excluded by `.gitignore`
- **Store certificates securely** with appropriate file permissions
- **Rotate certificates regularly** as per your organization's security policy
- **Use service-specific certificates** rather than personal certificates for production

## Troubleshooting

### Common Certificate Issues:

1. **"Certificate verify failed"**
   - Check that `root.pem` matches your Qlik server's certificate
   - Verify server URL matches certificate CN/SAN

2. **"SSL handshake failed"**
   - Ensure `client.pem` and `client_key.pem` are a matching pair
   - Check certificate hasn't expired

3. **"Access denied"**
   - Verify the client certificate has Engine API access
   - Check user directory and user ID configuration

### Testing Certificate Connection:

Use the provided test script:
```bash
python tests/test_qlik_connection.py
```

This will validate your certificate configuration and connection to Qlik Sense.

## Certificate Formats

The MCP server expects PEM format certificates. If you have certificates in other formats:

### Convert P12/PFX to PEM:
```bash
# Extract client certificate
openssl pkcs12 -in client.p12 -clcerts -nokeys -out client.pem

# Extract client private key  
openssl pkcs12 -in client.p12 -nocerts -nodes -out client_key.pem

# Extract root certificate
openssl pkcs12 -in client.p12 -cacerts -nokeys -out root.pem
```

### Convert DER to PEM:
```bash
openssl x509 -inform der -in certificate.der -out certificate.pem
```