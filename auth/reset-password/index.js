const User = require('../../models').users;
const mailgun = require('../../services/mailgun');
const config = require('../../config');
const mailInfo = require('./mail-info');

module.exports = app => {
  app.post('/reset-password', async(req, res) => {
    try {
      const token = req.body.token;
      const password = req.body.password;
      const user = await User.findOne({ token });
      if (!user) {
        return status(500).send({ error: config.locale.auth.token_invalid });
      }
      await user.update({ password, token: '' });
      res.status(500).send({ success: config.locale.success.global });
    } catch (error) {
      res.status(500).send({ error });
    }
  });

  app.post('/send-reset-password-mail', async (req, res) => {
    try {
      const email = req.body.email;

      const token = crypto.randomBytes(16).toString('hex');

      const user = await User.findOne({ where: { email: email } });

      if (!user) {
        return res.status(500).send({ error: config.locale.auth.failed });
      }

      await user.update({ token });

      await mailgun.messages().send(mailInfo({ email, token }));

      res.send(200, { success: config.locale.success.global });
    } catch (error) {
      return res.status(500).send({ error });
    }
  });
};
