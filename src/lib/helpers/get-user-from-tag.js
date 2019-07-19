const db = require('data/models');
module.exports = getUserFromTag = async tagId => {
	const tag = await db.tags.findByPk(tagId);
	const links = await tag.getLinks();
	const topics = await Promise.all(links.map(link => link.getTopic()));
  const user = await topics[0].getUser();
  return user;
};
