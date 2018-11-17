module.exports = {
  createTopic: async (_, { data: { title, links } }, { db, authUser }) => {
    try {
      return await db.topics.create(
        {
          title,
          user_id: 1,
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
      return await db.topics.update({ title: title }, { where: { id: id } });
    } catch (error) {
      throw new Error(error);
    }
  },

  deleteTopic: async (_, { data: { id } }, { db, authUser }) => {
    try {
      return await db.topics.destroy({ where: { id: id } });
    } catch (error) {
      throw new Error(error);
    }
  }
};
