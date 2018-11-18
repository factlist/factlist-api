const config = require('../config');
const jwt = require('jsonwebtoken');
const logger = require('../utils/logger');
module.exports = async (req, res, next) => {
  const token = req.headers['authorization'];
  if (token && token !== 'null') {
    try {
      const authUser = await jwt.verify(token, config.auth.jwtSecret);
      req.authUser = authUser;
    } catch (error) {
      logger.error(error);
    }
  }
  next();
};
