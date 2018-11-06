const faker = require('faker');
const _ = require('lodash');
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.bulkInsert(
      'tags',
      _.times(5, index => {
        return {
          id: index + 1,
          title: faker.random.word(),
          created_at: new Date(),
          updated_at: new Date()
        };
      })
    );
  },

  down: (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('tags', null, {});
  }
};
