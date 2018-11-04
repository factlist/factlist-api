module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('users', {
    name: DataTypes.STRING,
    username: DataTypes.STRING,
    email: DataTypes.STRING,
    password: DataTypes.STRING
  });
  User.associate = function(models) {
    User.hasMany(models.topics);
  };
  return User;
};
