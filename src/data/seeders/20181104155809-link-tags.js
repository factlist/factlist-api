const faker = require("faker")
const _ = require("lodash")

module.exports = {
	up: (queryInterface, Sequelize) => {
		return queryInterface.bulkInsert(
			"link_tags",
			_.times(5, index => {
				return {
					link_id: index + 1,
					tag_id: index + 1,
					created_at: new Date(),
					updated_at: new Date()
				}
			})
		)
	},

	down: (queryInterface, Sequelize) => {
		return queryInterface.bulkDelete("link_tags", null, {})
	}
}
