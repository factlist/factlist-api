module.exports = (sequelize, DataTypes) => {
  const Topic = sequelize.define('topics', {
    title: DataTypes.STRING,
    user_id: DataTypes.INTEGER
  });
  Topic.associate = function(models) {
    Topic.belongsTo(models.users);
    Topic.hasMany(models.links);
  };
  return Topic;
};
