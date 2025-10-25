# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: Send details to [security@sharekhan-mcp.com](mailto:security@sharekhan-mcp.com)
2. **GitHub Security Advisory**: Use GitHub's private vulnerability reporting feature

### What to Include

Please include the following information in your report:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

After you submit a report, we will:

1. Confirm receipt of your vulnerability report within 48 hours
2. Provide regular updates about our progress
3. Credit you in our security advisories (unless you prefer to remain anonymous)

### Security Best Practices

When using this package, please follow these security best practices:

#### API Credentials
- Never commit API credentials to version control
- Use environment variables for sensitive configuration
- Rotate credentials regularly
- Use different credentials for development and production

#### Network Security
- Use HTTPS in production environments
- Implement proper firewall rules
- Monitor API usage and access patterns
- Use secure WebSocket connections (WSS)

#### Authentication
- Complete the authentication flow before using trading tools
- Monitor token expiry and re-authenticate as needed
- Use strong, unique credentials
- Implement proper session management

#### Input Validation
- Validate all input data
- Use the built-in Pydantic validation
- Sanitize user inputs
- Implement rate limiting

#### Logging and Monitoring
- Enable structured logging
- Monitor for suspicious activities
- Set up alerts for unusual patterns
- Regularly review access logs

### Known Security Considerations

#### API Key Exposure
- API keys are sensitive and should be treated as passwords
- Never log API keys or include them in error messages
- Use environment variables or secure credential management systems

#### WebSocket Security
- WebSocket connections use authentication tokens
- Ensure tokens are properly validated
- Monitor for unauthorized connection attempts

#### Data Privacy
- The package may handle financial data
- Ensure compliance with relevant data protection regulations
- Implement proper data retention policies

### Security Updates

We will release security updates as needed. Please:

- Keep the package updated to the latest version
- Subscribe to security notifications
- Review security advisories
- Test updates in a non-production environment first

### Responsible Disclosure

We follow responsible disclosure practices:

- We will not publicly disclose vulnerabilities until they are patched
- We will work with you to coordinate the disclosure timeline
- We will credit security researchers who responsibly disclose vulnerabilities
- We will not take legal action against security researchers who follow these guidelines

### Contact

For security-related questions or concerns, please contact:

- **Security Team**: [security@sharekhan-mcp.com](mailto:security@sharekhan-mcp.com)
- **General Support**: [support@sharekhan-mcp.com](mailto:support@sharekhan-mcp.com)

Thank you for helping keep Sharekhan Connect MCP and our users safe!
