const { check } = require('../../../helpers');

module.exports = {
  users: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.users.findAll();
  },

  user: async (_, { username }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.users.findOne({
      where: { username }
    });
	},

	getUserById: async (_, { id }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.users.findOne({
      where: { id }
    });
  },

  topics: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.topics.findAll({
      include: [
        {
          model: db.users
        }
      ]
    });
  },

  links: async (_, args, { db, authUser }) => {
    check.Auth(authUser);
    return await db.links.findAll({
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
    return await db.tags.findAll();
  },

  tag: async (_, { id }, { db, authUser }) => {
    check.Auth(authUser);
    return await db.tags.findByPk(id);
  }
};
