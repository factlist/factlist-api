const jwt = require('jsonwebtoken');
module.exports = async (req, res, next) => {
  const token = req.headers['authorization'];
  if (token && token !== 'null') {
    try {
      const authUser = await jwt.verify(token, config.auth.jwtSecret);
      req.authUser = authUser;
    } catch (e) {
      console.log(e);
    }
  }
  next();
};
