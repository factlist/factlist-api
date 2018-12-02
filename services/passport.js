const passport = require('passport');
const User = require('../models').users;
const config = require('../config');
const JwtStrategy = require('passport-jwt').Strategy;
const ExtractJwt = require('passport-jwt').ExtractJwt;

const LocalStrategy = require('passport-local');

// Create local strategy
const localOptions = { usernameField: 'email' };
const localLogin = new LocalStrategy(
  localOptions,
  async (email, password, done) => {
    const user = await User.findOne({ where: { email: email } });

    if (!user) {
      return done(null, false);
    }

    const isMatch = await user.comparePassword(password);

    if (!isMatch) {
      return done(null, false);
    }

    return done(null, user);
  }
);

// Setup options for JWT Strategy
const jwtOptions = {
  jwtFromRequest: ExtractJwt.fromHeader('authorization'),
  secretOrKey: config.auth.jwtSecret
};

// Create JWT strategy
const jwtLogin = new JwtStrategy(jwtOptions, async (payload, done) => {
  try {
    const user = await User.findByPk(payload.sub);
    if (user) {
      return done(null, true);
    }
    return done(null, false);
  } catch (err) {
    return done(err, false);
  }
});

passport.use(jwtLogin);
passport.use(localLogin);
