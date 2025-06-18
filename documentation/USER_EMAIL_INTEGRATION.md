# User Email Integration for Email Agent

## Overview

The email agent has been enhanced to automatically send trend reports to the logged-in user's email address instead of relying solely on GitHub secrets or environment variables.

## How It Works

### Email Recipient Priority Order

The email agent now uses the following priority order when determining where to send reports:

1. **Logged-in User Email** (Highest Priority)
   - When a user is authenticated via Google OAuth2, their email address is automatically used
   - No configuration required - works out of the box

2. **Function Parameter** (Medium Priority)  
   - If `recipient_email` parameter is explicitly provided to the `send_email_report` function

3. **Environment Variable** (Lowest Priority)
   - Falls back to `EMAIL_RECIPIENTS` environment variable
   - Supports multiple comma-separated recipients

### Technical Implementation

The system uses thread-local storage to pass the authenticated user's email from the web middleware to the email agent:

```python
# In the middleware
user_info = request.state.user  # Set by OAuth2 middleware
if user_info and user_info.get('email'):
    set_current_user_email(user_info['email'])

# In the email agent  
user_email = get_current_user_email()
if user_email:
    recipients = [user_email.strip()]  # Use logged-in user's email
```

### Files Modified

1. **`trend_spotter/sub_agents/email_agent.py`**
   - Added thread-local storage for user context
   - Added `set_current_user_email()` and `get_current_user_email()` functions
   - Modified `send_email_report()` to prioritize user email

2. **`user_context_middleware.py`** (New)
   - Middleware to capture user email from OAuth2 session
   - Sets user email in thread-local storage

3. **`authenticated_server.py`**
   - Updated to include the new user context middleware

## Benefits

### For Users
- ✅ **Zero Configuration**: No need to set up `EMAIL_RECIPIENTS` for personal use
- ✅ **Automatic**: Reports automatically go to the logged-in user
- ✅ **Secure**: Uses authenticated user context, no hardcoded emails

### For Developers  
- ✅ **Backward Compatible**: Existing `EMAIL_RECIPIENTS` configuration still works
- ✅ **Flexible**: Can still override with explicit recipient parameters
- ✅ **Clean Architecture**: Uses standard web middleware patterns

## Usage Examples

### Scenario 1: Personal Use (Most Common)
```bash
# User logs in via Google OAuth2 as john@company.com
# Requests a trend report through the web UI
# Email automatically sent to john@company.com
# No configuration needed!
```

### Scenario 2: Team Distribution (Legacy)
```bash
# Set environment variable for team distribution
export EMAIL_RECIPIENTS="team@company.com,manager@company.com"
# Reports go to team emails when no user is logged in
```

### Scenario 3: Programmatic Use
```python
# Explicit recipient override
send_email_report(
    subject="Custom Report",
    report_content="...",
    recipient_email="specific@recipient.com"  # Overrides user context
)
```

## Testing

Run the test suite to verify the priority logic:

```bash
python test_user_email_priority.py
```

Expected output:
```
🎉 ALL TESTS PASSED!

Summary:
✅ User email context takes priority over environment variables  
✅ Environment variables work as fallback when no user context
✅ Parameter-based recipient works when no user context
✅ Priority order: User Context > Parameter > Environment
```

## Migration Notes

### For Existing Users
- **No action required** - the system maintains backward compatibility
- Existing `EMAIL_RECIPIENTS` environment variables continue to work as fallback
- When users log in via OAuth2, their personal email takes priority

### For New Users
- Simply log in via Google OAuth2 - no email configuration needed
- The system automatically sends reports to the authenticated user's email
- Optional: Set `EMAIL_RECIPIENTS` for team distribution scenarios

## Security Considerations

- User email is only accessible within the same HTTP request thread
- Thread-local storage prevents email leakage between different user sessions  
- OAuth2 middleware ensures only authenticated users can trigger email delivery
- No sensitive information is logged or exposed

## Troubleshooting

### Issue: Reports not going to logged-in user
**Cause**: User context middleware not properly configured
**Solution**: Ensure `authenticated_server.py` includes both auth and user context middleware

### Issue: Thread-local storage not working
**Cause**: Different thread handling between request and agent execution
**Solution**: Verify middleware order - user context must come after OAuth2 auth

### Issue: Multiple recipients not working
**Cause**: User context overrides environment variable
**Solution**: Either log out or clear user context for multi-recipient scenarios

---

**🎯 Result**: The email agent now provides a seamless experience where authenticated users automatically receive reports at their logged-in email address, while maintaining full backward compatibility with existing configurations!

