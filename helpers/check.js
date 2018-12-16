const config = require('../config');
const check = {
  Auth: authUser => {
    if (!authUser) {
      throw new Error(config.locale.auth.not_authorized);
    }
  }
};

module.exports = check;
