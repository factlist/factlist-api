const jwt = require('jsonwebtoken');
const config = require('../config');

const token = {
  generate: ({ id }, expiresIn) => {
    return jwt.sign({ sub: id }, config.auth.jwtSecret, { expiresIn });
  }
};

module.exports = token;
