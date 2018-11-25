const User = require('../models').users;
const token = require('../helpers/token');
const config = require('../config');
module.exports = app => {
  app.post('/register', async (req, res) => {
    if (!req.body.email || !req.body.password) {
      return res
        .status(422)
        .send({ error: 'You must provide email and password' });
    }
    const user = await User.findOne({ where: { email: req.body.email } });

    if (user) {
      return res.status(422).send({ error: 'Email is in use' });
    }
    const createdUser = await User.create(req.body);
    res.send({
      token: token.generate({ id: createdUser.id }, config.auth.tokenLifeTime)
    });
  });
};
