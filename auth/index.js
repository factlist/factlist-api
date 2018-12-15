const Login = require('./login');
const Register = require('./register');
const Twitter = require('./twitter');
const ResetPassword = require('./reset-password');

module.exports = app => {
  Login(app);
  Register(app);
  Twitter(app);
  ResetPassword(app);
};
