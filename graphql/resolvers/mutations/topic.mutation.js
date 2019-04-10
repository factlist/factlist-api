const { check } = require('../../../helpers/');

module.exports = {
  createTopic: async (_, { data: { title = "Untitled topic", links = [] } }, { db, authUser }) => {
    
    //TODO validate both title or link is empty.
      
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
			topic.user = authUser.get({plain:true});
			return topic;

    } catch (error) {
      throw new Error(error);
    }
  },

  updateTopicTitle : async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const topic = await db.topics.findOne({
        where : { id: id, user_id: authUser.id }
      });
      await topic.update({
        title : title
      });

      return topic;
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
