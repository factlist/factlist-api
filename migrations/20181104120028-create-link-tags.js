module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('link_tags', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      link_id: {
        type: Sequelize.INTEGER
      },
      tag_id: {
        type: Sequelize.INTEGER
      },
      created_at: {
				allowNull: false,
				type: Sequelize.DATE,
			},
			updated_at: {
				allowNull: false,
				type: Sequelize.DATE,
			},
			deleted_at: {
				allowNull: true,
				type: Sequelize.DATE,
				field: "deleted_at",
			},
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('link_tags');
  }
};
