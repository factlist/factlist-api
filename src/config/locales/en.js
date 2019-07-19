module.exports = {
  error: {
    global: 'An error occurred!'
  },
  success: {
    global: 'ok'
  },
  auth: {
    not_authorized: 'You are not authorized.',
    must_provide_email: 'You must provide email and password.',
    already_use_email: 'Email is in use.',
    failed: 'These credentials do not match our records.',
    send_reset_password_mail: 'Reset password mail has been sent successfully.',
    token_invalid: 'Password reset token is invalid.',
    incorrect_password: 'Incorrect password.'
  },
  mailer: {
    reset_password_email_subject: 'Reset your password',
    reset_password_email_content:
      'Hey,<br> did you forget your password? Click the <a href="http://faclist.com/reset-password?token=:token">link</a> to reset it.'
  }
};
