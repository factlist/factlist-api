const db = require('../models');

const getUserFromLink = async LinkId => {
  const link = await db.links.findByPk(linkId);
  const topic = await link.getTopic();
  return await topic.getUser();
};

const getUserFromTag = async tagId => {
  const tag = await db.tags.findByPk(tagId);
  const links = await tag.getLinks();
  const topics = await Promise.all(links.map(link => link.getTopic()));
  const user = await topics[0].getUser();
  return user;
};

module.exports = {
  getUserFromLink,
  getUserFromTag
};
