const bcrypt = require('bcryptjs');

module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define(
    'users',
    {
      name: DataTypes.STRING,
      username: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
      },
      email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
      },
      password: DataTypes.STRING,
      twitter: DataTypes.STRING
    },
    {
      hooks: {
        beforeCreate: async user => {
          const hashedPassword = await bcrypt.hash(user.password, 10);
          user.password = hashedPassword;
        }
      }
    }
  );

  User.prototype.comparePassword = function(password) {
    return bcrypt.compare(password, this.password);
  };

  User.associate = function(models) {
    User.hasMany(models.topics);
  };
  return User;
};
