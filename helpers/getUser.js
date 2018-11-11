const User = require('../models').users;

module.exports = async id => {
  const user = await User.findByPk(id);
  return user.get({ plain: true });
};
