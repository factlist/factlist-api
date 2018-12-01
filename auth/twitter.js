const User = require('../models').users;
const passport = require('passport');
const TwitterStrategy = require('passport-twitter').Strategy;
const config = require('../config');

const twitterOptions = { ...config.auth.twitter, passReqToCallback: true };

passport.use(
  new TwitterStrategy(
    twitterOptions,
    async (req, token, tokenSecret, profile, done) => {
      const user = await User.findOrCreate({
        where: { twitter: profile.id, username: profile.screen_name }
      });
      done(null, user);
    }
  )
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

module.exports = app => {
  app.get('/auth/twitter', passport.authenticate('twitter'));
  app.get(
    '/auth/twitter/callback',
    passport.authenticate('twitter', { failureRedirect: '/login' }),
    function(req, res) {
      res.redirect('/');
    }
  );
};
