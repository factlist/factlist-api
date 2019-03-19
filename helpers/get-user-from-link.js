const db = require('../models');
module.exports = getUserFromLink = async linkId => {
  const link = await db.links.findByPk(linkId);
  const topic = await link.getTopic();
  return await topic.getUser();
};
