const token = require('lib/helpers/token');
const passport = require('passport');
const requireSignin = passport.authenticate('local', { session: false });
const config = require('config');
require('lib/services/passport');

module.exports = app => {
  app.post('/api/v1/auth/login', requireSignin, (req, res) => {
    res.send({
      token: token.generate({ id: req.user.id }, config.auth.tokenLifeTime)
    });
  });
};
