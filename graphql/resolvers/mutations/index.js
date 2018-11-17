const user = require('./user.mutation');
const link = require('./link.mutation');
const tag = require('./tag.mutation');
const topic = require('./topic.mutation');

const Mutation = {
  ...user,
  ...link,
  ...tag,
  ...topic
};

module.exports = Mutation;
