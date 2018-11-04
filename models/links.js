module.exports = (sequelize, DataTypes) => {
  const links = sequelize.define(
    'links',
    {
      title: DataTypes.STRING,
      url: DataTypes.STRING,
      topic_id: DataTypes.INTEGER
    },
    {}
  );
  links.associate = function(models) {
    // associations can be defined here
  };
  return links;
};
