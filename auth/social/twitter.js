const User = require('../../models').users;
const passport = require('passport');
const TwitterStrategy = require('passport-twitter').Strategy;
const config = require('../../config');
const token = require('../../helpers/token');

const twitterOptions = { ...config.auth.twitter, passReqToCallback: true };

const twitterStrategy = new TwitterStrategy(
  twitterOptions,
  async (req, token, tokenSecret, profile, done) => {
    try {
      let user = await User.findOne({ where: { twitter: profile.id } });
      if (!user) {
        user = User.create({
          twitter: profile.id,
          username: profile.username,
          name: profile.displayName,
          email: profile.emails[0].value
        });
      }
      done(null, user);
    } catch (error) {
      done(error, false);
    }
  }
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

module.exports = app => {
  app.get('/auth/twitter', passport.authenticate('twitter'));
  app.get(
    '/auth/twitter/callback',
    passport.authenticate('twitter', { failureRedirect: '/login' }),
    handleSocialAuth
  );
};

const handleSocialAuth = (req, res) => {
  if (!req.user) {
    return res.send(config.locale.auth.not_authorized);
  }
  return res.send({
    token: token.generate({ id: req.user.id }, config.auth.tokenLifeTime)
  });
};

passport.use(twitterStrategy);
