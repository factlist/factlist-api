const Login = require('./local/login');
const Register = require('./local/register');
const Twitter = require('./social/twitter');
const ResetPassword = require('./reset-password');

module.exports = app => {
  Login(app);
  Register(app);
  Twitter(app);
  ResetPassword(app);
};
