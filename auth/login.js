const token = require('../helpers/token');
const passport = require('passport');
const requireSignin = passport.authenticate('local', { session: false });
const config = require('../config');
require('../services/passport');

module.exports = app => {
  app.post('/login', requireSignin, (req, res) => {
    res.send({
      token: token.generate({ id: req.user.id }, config.auth.tokenLifeTime)
    });
  });
};
