module.exports = {
  updateLink: async (_, { data: { id, title, url } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.links.update(
        { title: title, url: url },
        { where: { id: id } }
      );
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteLink: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.links.destroy({ where: { id: id } });
    } catch (error) {
      throw new error();
    }
  }
};
