const passport = require('passport');
const TwitterStrategy = require('passport-twitter').Strategy;
const config = require('../config');

const twitterOptions = { ...config.auth.twitter, passReqToCallback: true };

passport.use(
  new TwitterStrategy(
    twitterOptions,
    async (token, tokenSecret, profile, done) => {
      User.findOrCreate({ twitter: profile.id }, (err, user) => {
        return done(err, user);
      });
    }
  )
);

module.exports = app => {
  app.get('/auth/twitter', passport.authenticate('twitter'));
  app.get(
    '/auth/twitter/callback',
    passport.authenticate('twitter', {
      successRedirect: '/test',
      failureRedirect: '/'
    })
  );
};
