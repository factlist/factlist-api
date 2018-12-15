const config = require('../config');
module.exports = require('mailgun-js')({
  apiKey: config.auth.mailgunApiKey,
  domain: config.auth.mailgunDomain
});
