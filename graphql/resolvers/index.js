// query resolvers
const Query = require('./queries/Query');
const Topic = require('./queries/Topic');
const Link = require('./queries/Link');
const User = require('./queries/User');

// mutation resolvers
const Mutation = require('./mutations/index');

module.exports = {
  Query,
  Topic,
  User,
  Link,
  Mutation
};
