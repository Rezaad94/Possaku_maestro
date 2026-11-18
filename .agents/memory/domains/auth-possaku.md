# Domain Intelligence: Authentication & Test Accounts

- **Domain**: User Identity & POS Access Credentials
- **Context**: Possaku Point of Sale System

---

## 1. Test Accounts & Environments

Stored in `pages/login/login_credential.js`:

```javascript
output.login_credential = {
  dev: {
    validPhoneNumber: "081234567890",
    validPhoneNumber2: "089876543210",
    validPIN: "123456",
    invalidPIN: "000000"
  }
};
```

---

## 2. Authentication Rules
- **Phone Number Format**: Accepts Indonesian standard formats (`08...` or `+62...`).
- **PIN Requirements**: 6-digit numeric security PIN entered on a custom numeric pad.
- **Session Persistence**: Logging in retains local token state until `- clearState` is invoked. Top-level test suites should always clean state at start to guarantee determinism.

