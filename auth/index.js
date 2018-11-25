const Login = require('./login');
const Register = require('./register');
const Twitter = require('./twitter');

module.exports = app => {
  Login(app);
  Register(app);
  Twitter(app);
};
