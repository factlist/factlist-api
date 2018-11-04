module.exports = (sequelize, DataTypes) => {
  const users = sequelize.define(
    'users',
    {
      name: DataTypes.STRING,
      username: DataTypes.STRING,
      email: DataTypes.STRING,
      password: DataTypes.STRING
    },
    {}
  );
  users.associate = function(models) {
    // associations can be defined here
  };
  return users;
};
