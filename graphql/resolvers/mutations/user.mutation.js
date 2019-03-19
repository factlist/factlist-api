const bcrypt = require('bcryptjs');
const config = require('../../../config/');
const { token, check } = require('../../../helpers');

module.exports = {
  login: async (_, { data: { email, password } }, { db }) => {
    try {
      const user = await db.users.findOne({ where: { email } });
      if (!user) {
        throw new Error(config.locale.auth.failed);
      }
      const valid = await bcrypt.compare(password, user.password);
      if (!valid) {
        throw new Error(config.locale.auth.incorrect_password);
      }
      return { token: token.generate(user, '1h') };
    } catch (error) {
      throw new Error(error);
    }
  },

  createUser: async (_, args, { db }) => {
    try {
      const user = await db.users.create({
        name: args.data.name,
        username: args.data.username,
        email: args.data.email,
        password: await bcrypt.hash(args.data.password, 10)
      });
      return { token: token.generate(user, '1h') };
    } catch (error) {
      throw new Error(error);
    }
  },

  updateUser: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    try {
      const user = await db.users.findByPk(args.data.id);
      await user.update({
        name: args.data.name,
        username: args.data.username,
        email: args.data.email,
        password: await bcrypt.hash(args.data.password, 10)
      });
      return user;
    } catch (error) {
      throw new Error(error);
    }
  }
};
