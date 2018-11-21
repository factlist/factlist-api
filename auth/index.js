const passport = require('passport');
const User = require('../models').users;
const token = require('../helpers/token');
const requireAuth = passport.authenticate('jwt', { session: false });
const requireSignin = passport.authenticate('local', { session: false });
require('../services/passport');

module.exports = app => {
  app.get('/', requireAuth, (req, res) => {
    res.send({ hi: 'there' });
  });

  app.post('/login', requireSignin, (req, res) => {
    res.send({ token: token.generate({ id: req.user.id }, '1h') });
  });

  app.post('/register', async (req, res) => {
    const email = req.body.email;
    const password = req.body.password;
    const username = req.body.username;
    const name = req.body.name;

    if (!email || !password) {
      return res
        .status(422)
        .send({ error: 'You must provide email and password' });
    }

    const user = await User.findOne({ where: { email: email } });

    if (user) {
      return res.status(422).send({ error: 'Email is in use' });
    }

    const createdUser = await User.create({
      name,
      username,
      email,
      password
    });

    res.send({ token: token.generate({ id: createdUser.id }, '1h') });
  });
};
