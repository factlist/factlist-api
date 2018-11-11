const jwt = require('jsonwebtoken');
const config = require('../../config');
const getToken = require('../../helpers/getToken');
const getUser = require('../../helpers/getUser');

const AuthUser = async req => {
  const token = getToken(req.headers.authorization);
  const { sub } = await jwt.verify(token, config.auth.jwtSecret);

  if (!sub) throw new Error('No Tenant');

  return await getUser(sub);
};

module.exports = AuthUser;
