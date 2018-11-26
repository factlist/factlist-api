const check = require('../../../helpers/check');

module.exports = {
  createTopic: async (_, { data: { title, links } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.topics.create(
        {
          title,
          user_id: authUser.sub,
          links
        },
        {
          include: [
            {
              model: db.links,
              include: [{ model: db.tags }]
            }
          ]
        }
      );
    } catch (error) {
      throw new Error(error);
    }
  },

  updateTopic: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.topics.update({ title: title }, { where: { id: id } });
    } catch (error) {
      throw new Error(error);
    }
  },

  deleteTopic: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.topics.destroy({
        where: { id: id, user_id: authUser.sub }
      });
    } catch (error) {
      throw new Error(error);
    }
  }
};
