module.exports = (sequelize, DataTypes) => {
  const LinkTag = sequelize.define('link_tags', {
    link_id: DataTypes.INTEGER,
    topic_id: DataTypes.INTEGER
  });
  return LinkTag;
};
