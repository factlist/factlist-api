module.exports = (sequelize, DataTypes) => {
  const Link = sequelize.define('links', {
    title: DataTypes.STRING,
    url: DataTypes.STRING,
    topic_id: DataTypes.INTEGER
  });
  Link.associate = function(models) {
		Link.belongsTo(models.topics);
    Link.belongsToMany(models.tags, { through: models.link_tags });
  };
  return Link;
};
