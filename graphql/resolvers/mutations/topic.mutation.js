const { check } = require('../../../helpers/');

module.exports = {
  createTopic: async (_, { data: { title, links } }, { db, authUser }) => {
    try {
			check.Auth(authUser);
      let topic=  await db.topics.create(
        {
          title,
          user_id: authUser.id,
          links,
        },
        {
          include: [
            { model: db.users },
            {
              model: db.links,
              include: [{ model: db.tags }]
            }
          ]
        }
			);
			topic = topic.get({plain:true});
			topic.user = authUser.get({plain:true});
			return topic;

    } catch (error) {
      throw new Error(error);
    }
  },

  updateTopic: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.topics.update(
        { title: title },
        { where: { id: id, user_id: authUser.id } }
      );
    } catch (error) {
      throw new Error(error);
    }
  },

  deleteTopic: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.topics.destroy({
        where: { id: id, user_id: authUser.id }
      });
    } catch (error) {
      throw new Error(error);
    }
  }
};
