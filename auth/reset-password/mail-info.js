const config = require('../../config');
const { attrReplacer } = require('../../helpers');
module.exports = ({ email, token }) => {
  return {
    from: config.auth.mailgunAccountEmail,
    to: email,
    subject: config.locale.mailer.reset_password_email_subject,
    html: attrReplacer(config.locale.mailer.reset_password_email_content, {
      ':token': token
    })
  };
};
