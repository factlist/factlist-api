const { check } = require('../../../helpers');

module.exports = {
  users: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.users.all();
  },

  user: async (_, { username }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.users.find({
      where: { username }
    });
  },

  topics: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.topics.all({
      include: [
        {
          model: db.users
        }
      ]
    });
  },

  topic: async (_, { id }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.topics.findByPk(id);
  },

  tags: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.tags.all();
  },

  tag: async (_, { id }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.tags.findByPk(id);
  }
};
