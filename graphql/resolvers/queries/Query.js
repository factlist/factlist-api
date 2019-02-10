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

	getUserById: async (_, { id }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.users.find({
      where: { id }
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

  links: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.links.all({
      include: [
        {
          model: db.topics
        },
        {
          model: db.tags
        }
      ]
    });
  },

  link: async (_, { id }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.links.findByPk(id);
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
