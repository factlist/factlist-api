const User = require('../../models').users;
const token = require('../../helpers/token');
const config = require('../../config');
module.exports = app => {
  app.post('/auth/register', async (req, res) => {
    if (!req.body.email || !req.body.password) {
      return res
        .status(500)
        .send({ error: config.locale.auth.must_provide_email });
    }
    const user = await User.findOne({ where: { email: req.body.email } });

    if (!user) {
      return res
        .status(500)
        .send({ error: config.locale.auth.already_use_email });
    }
    const createdUser = await User.create(req.body);
    res.send({
      token: token.generate({ id: createdUser.id }, config.auth.tokenLifeTime)
    });
  });
};
