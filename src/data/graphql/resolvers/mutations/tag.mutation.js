const { check, getUserFromTag } = require('lib/helpers');
const config = require('config');

module.exports = {
  updateTag: async (_, { data: { id, title } }, { db, authUser }) => {
    try {
			check.Auth(authUser);
			const user = await getUserFromTag(id);
      if (authUser.id === user.id) {
        return await db.tags.update({ title: title }, { where: { id: id } });
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new Error(error);
    }
  },
  deleteTag: async (_, { data: { id } }, { db, authUser }) => {
    try {
      check.Auth(authUser);
      const user = await getUserFromTag(id);
      if (authUser.id === user.id) {
        return await db.tags.destroy({ where: { id: id } });
      }
      throw new Error(config.locale.auth.not_authorized);
    } catch (error) {
      throw new error();
    }
  }
};
