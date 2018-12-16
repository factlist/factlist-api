const { getUserFromTopic, check } = require('../../../helpers/');
const config = require('../../../config/');

module.exports = {
  createLink: async (
    _,
    { data: {title, url, topic_id, tags } },
    { db, authUser }
  ) => {
    try {
			check.Auth(authUser);
			const topic = await db.topics.findByPk(topic_id);
      if (authUser.id === topic.user_id) {
        return await db.links.create(
          { title, url, topic_id, tags },
          {
            include: [{ model: db.tags }]
          }
        );
			}
			throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },
  updateLink: async (_, { data: { id, title, url } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {
        return await db.links.update(
          { title: title, url: url },
          { where: { id: id } }
        );
			}
			throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteLink: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.id === user.id) {
        return await db.links.destroy({ where: { id: id } });
			}
			throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  }
};
