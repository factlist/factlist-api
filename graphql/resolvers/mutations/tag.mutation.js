const check = require('../../../helpers/check');
const { getUserFromTag } = require('../../../helpers/get-user');

module.exports = {
  updateTag: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromTag(id);
      if (authUser.sub === user.id) {
        return await db.tags.update({ title: title }, { where: { id: id } });
      }
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteTag: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromTag(id);
      if (authUser.sub === user.id) {
        return await db.tags.destroy({ where: { id: id } });
      }
    } catch (error) {
      throw new error();
    }
  }
};
