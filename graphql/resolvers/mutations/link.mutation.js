module.exports = {
  updateLink: async (_, { data: { id, title, url } }, { db, authUser }) => {
    try {
      return await db.links.update(
        { title: title, url: url },
        { where: { id: id } }
      );
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteLink: async (_, { data: { id } }, { authUser }) => {
    try {
      return await db.links.destroy({ where: { id: id } });
    } catch (error) {
      throw new error();
    }
  }
};
