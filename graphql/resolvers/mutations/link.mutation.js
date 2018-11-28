const check = require('../../../helpers/check');
const { getUserFromLink } = require('../../../helpers/get-user');

module.exports = {
  createLink: async (
    _,
    { data: { id, title, url, tags } },
    { db, authUser }
  ) => {
    try {
      check.Auth(authUser);
      if (authUser.sub === user.id) {
        return await db.links.create(
          {
            title,
            url,
            tags
          },
          {
            include: [{ model: db.tags }]
          }
        );
      }
    } catch (error) {
      throw new Error(error);
    }
  },
  updateLink: async (_, { data: { id, title, url } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.sub === user.id) {
        return await db.links.update(
          { title: title, url: url },
          { where: { id: id } }
        );
      }
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteLink: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromLink(id);
      if (authUser.sub === user.id) {
        return await db.links.destroy({ where: { id: id } });
      }
    } catch (error) {
      throw new Error(error);
    }
  }
};
