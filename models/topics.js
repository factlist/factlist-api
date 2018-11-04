module.exports = (sequelize, DataTypes) => {
  const topics = sequelize.define(
    'topics',
    {
      title: DataTypes.STRING,
      user_id: DataTypes.INTEGER
    },
    {}
  );
  topics.associate = function(models) {
    // associations can be defined here
  };
  return topics;
};
