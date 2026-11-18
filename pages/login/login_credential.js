// ==============================================================================
// Possaku Mobile Automation - Login Credentials Resolver
// Reads dynamically from Maestro Environment Variables (-e / config/env.yaml)
// ZERO hardcoded sensitive credentials in source code.
// ==============================================================================

var resolvedPhone = (typeof PHONE_NUMBER !== 'undefined' && PHONE_NUMBER) ? String(PHONE_NUMBER) : "";
var resolvedPIN = (typeof PIN !== 'undefined' && PIN) ? String(PIN) : "";
var invalidPhone = (typeof INVALID_PHONE !== 'undefined' && INVALID_PHONE) ? String(INVALID_PHONE) : "080000000000";
var invalidPin = (typeof INVALID_PIN !== 'undefined' && INVALID_PIN) ? String(INVALID_PIN) : "000000";
var inactivePhone = (typeof INACTIVE_PHONE !== 'undefined' && INACTIVE_PHONE) ? String(INACTIVE_PHONE) : "080000000001";

// Format helper: Normalize to '08...' and '+628...'
var cleanDigits = resolvedPhone.replace(/[^0-9]/g, "");
var phoneZero = resolvedPhone ? (cleanDigits.startsWith("62") ? ("0" + cleanDigits.substring(2)) : (cleanDigits.startsWith("0") ? cleanDigits : ("0" + cleanDigits))) : "";
var phonePlus = (phoneZero && phoneZero.length > 1) ? ("+62" + phoneZero.substring(1)) : "";

output.login_credential = {
  dev: {
    validPhoneNumber1: phoneZero,
    validPhoneNumber2: phonePlus,
    validPIN: resolvedPIN,
    invalidPhoneNumber: invalidPhone,
    invalidPIN: invalidPin,
    inactiveUserPhoneNumber: inactivePhone,
  },
  staging: {
    validPhoneNumber1: phoneZero,
    validPhoneNumber2: phonePlus,
    validPIN: resolvedPIN,
    invalidPhoneNumber: invalidPhone,
    invalidPIN: invalidPin,
    inactiveUserPhoneNumber: inactivePhone,
  },
  prod: {
    validPhoneNumber1: phoneZero,
    validPhoneNumber2: phonePlus,
    validPIN: resolvedPIN,
    invalidPhoneNumber: invalidPhone,
    invalidPIN: invalidPin,
    inactiveUserPhoneNumber: inactivePhone,
  }
};
