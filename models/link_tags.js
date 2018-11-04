module.exports = (sequelize, DataTypes) => {
  const link_tags = sequelize.define(
    'link_tags',
    {
      link_id: DataTypes.INTEGER,
      topic_id: DataTypes.INTEGER
    },
    {}
  );
  link_tags.associate = function(models) {
    // associations can be defined here
  };
  return link_tags;
};
