const User = require('data/models').users;
const passport = require('passport');
const TwitterStrategy = require('passport-twitter').Strategy;
const config = require('config');
const token = require('lib/helpers/token');

const platform = 'twitter';
const authRouter = '/api/v1/auth/twitter';
const callbackRouter = '/api/v1/auth/twitter/callback';
const failureRedirect = '/login';
const authMiddleware = passport.authenticate(platform, { failureRedirect });
const twitterOptions = { ...config.auth.twitter, passReqToCallback: true };

const userData = profile => {
  return {
    twitter: profile.id,
    username: profile.username,
    name: profile.displayName,
    email: profile.emails[0].value
  };
};

const twitterStrategy = new TwitterStrategy(
  twitterOptions,
  async (req, token, tokenSecret, profile, done) => {
    try {
      let user = await User.findOne({ where: { twitter: profile.id } });
      if (!user) {
        user = await User.create(userData(profile));
      }
      done(null, user);
    } catch (error) {
      done(error, false);
    }
  }
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

const handleSocialAuth = (req, res) => {
  if (!req.user) {
    return res.send(config.locale.auth.not_authorized);
  }
  return res.send({
    token: token.generate({ id: req.user.id }, config.auth.tokenLifeTime)
  });
};

module.exports = app => {
  app.get(authRouter, passport.authenticate(platform));
  app.get(callbackRouter, authMiddleware, handleSocialAuth);
};

passport.use(twitterStrategy);
