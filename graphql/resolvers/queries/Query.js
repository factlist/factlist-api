module.exports = {
  users: async (_, args, { db }) => {
    return await db.users.all();
  },

  user: async (_, { id }, { db }) => {
    return await db.users.findByPk(id);
  },

  topics: async (_, args, { db }) => {
    return await db.topics.all();
  },

  topic: async (_, { id }, { db }) => {
    return await db.topics.findByPk(id);
  },

  tags: async (_, args, { db }) => {
    return await db.tags.all();
  },

  tag: async (_, { id }, { db }) => {
    return await db.tags.findByPk(id);
  }
};
