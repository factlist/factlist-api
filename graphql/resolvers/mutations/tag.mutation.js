module.exports = {
  updateTag: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.tags.update({ title: title }, { where: { id: id } });
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteTag: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      return await db.tags.update({ where: { id: id } });
    } catch (error) {
      throw new error();
    }
  }
};
