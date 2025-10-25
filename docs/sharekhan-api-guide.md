# Sharekhan API Credentials Guide

A comprehensive step-by-step guide to obtain API credentials for Sharekhan trading APIs.

## 📋 Prerequisites

- Active Sharekhan trading account
- TOTP (Two-Factor Authentication) enabled
- Access to Sharekhan Developer Portal

## 🚀 Step-by-Step Guide

### Step 1: Access the Developer Portal

1. **Visit the Sharekhan Developer Portal:**
   - URL: [https://newtrade.sharekhan.com/skweb/login/trading-api](https://newtrade.sharekhan.com/skweb/login/trading-api)

2. **Log in to your account:**
   - Use your Sharekhan Client ID
   - Enter your password
   - Complete TOTP (Two-Factor Authentication) verification

### Step 2: Create a New API Application

1. **Navigate to App Creation:**
   - Once logged in, select **"Create New App"**

2. **Choose Application Type:**
   - Select **"Partner App"** option

3. **Configure Your Application:**
   - Enter your chosen **App Name** (e.g., "MyTradingApp")
   - Click **"Create"** to proceed

### Step 3: Generate and Secure Your API Keys

1. **Retrieve API Credentials:**
   - After creation, the portal will display your:
     - **API Key**
     - **Secret Key**

2. **Secure Storage:**
   - Copy and store both keys safely
   - These credentials are required for authentication in your trading application
   - ⚠️ **Important:** Never share these keys or commit them to version control

### Step 4: Enable TOTP (Two-Factor Authentication)

1. **Access Account Settings:**
   - Go to your Sharekhan account settings
   - Navigate to **"Change My 2FA/TOTP"**
   - Click **"Enable TOTP"**

2. **Save TOTP Key:**
   - Store the TOTP key securely
   - This is needed for integration with APIs or algorithmic platforms like:
     - AlgoDelta
     - Algomojo

### Step 5: Validate API Access

1. **Test Login Endpoint:**
   - Use the following endpoint to validate your credentials:
   ```
   https://api.sharekhan.com/skapi/auth/login.html?api_key=<YOUR_API_KEY>
   ```

2. **Additional Parameters:**
   - You may need to pass additional parameters based on your integration method:
     - `vendor_key` - For vendor-specific integrations
     - `state` - For OAuth state parameter

## 🔧 Integration Notes

- **API Version:** Check the latest API version requirements
- **Rate Limits:** Be aware of API rate limiting policies
- **Sandbox Testing:** Use sandbox environment for testing before production

## 🛡️ Security Best Practices

- ✅ Store credentials in environment variables
- ✅ Use secure credential management systems
- ✅ Never hardcode API keys in source code
- ✅ Regularly rotate API keys
- ✅ Monitor API usage and access logs

## 📞 Support

For additional help with API credentials:
- **Sharekhan Support:** Contact Sharekhan customer support
- **Documentation:** Refer to official Sharekhan API documentation
- **Community:** Check Sharekhan developer community forums

---

**Next Steps:** Once you have your API credentials, proceed to the [Configuration Guide](docs/CONFIGURATION.md) to set up your Sharekhan Connect MCP server.