module.exports = {
	up: (queryInterface, Sequelize) => {
		return queryInterface.createTable("topics", {
			id: {
				allowNull: false,
				autoIncrement: true,
				primaryKey: true,
				type: Sequelize.INTEGER
			},
			title: {
				type: Sequelize.STRING
			},
			user_id: {
				type: Sequelize.INTEGER
			},
			created_at: {
				allowNull: false,
				type: Sequelize.DATE
			},
			updated_at: {
				allowNull: false,
				type: Sequelize.DATE
			},
			deleted_at: {
				allowNull: true,
				type: Sequelize.DATE,
				field: "deleted_at"
			}
		})
	},
	down: queryInterface => {
		return queryInterface.dropTable("topics")
	}
}
