const faker = require("faker")
const _ = require("lodash")
module.exports = {
	up: (queryInterface, Sequelize) => {
		return queryInterface.bulkInsert(
			"topics",
			_.times(5, index => {
				return {
					id: index + 1,
					title: faker.random.word(),
					user_id: 1,
					created_at: new Date(),
					updated_at: new Date()
				}
			})
		)
	},

	down: (queryInterface, Sequelize) => {
		return queryInterface.bulkDelete("topics", null, {})
	}
}
