module.exports = {
  updateTag: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      return await db.tags.update({ title: title }, { where: { id: id } });
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteTag: async (_, { data: { id } }, { authUser }) => {
    try {
      return await db.tags.update({ where: { id: id } });
    } catch (error) {
      throw new error();
    }
  }
};
