module.exports = (sequelize, DataTypes) => {
	const Tag = sequelize.define("tags", {
		title: DataTypes.STRING
	})
	Tag.associate = function(models) {
		Tag.belongsToMany(models.links, { through: models.link_tags })
	}
	return Tag
}
