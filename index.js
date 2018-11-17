const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const { importSchema } = require('graphql-import');
const logger = require('./utils/logger');
const db = require('./models');
const config = require('./config');
const resolvers = require('./graphql/resolvers');

const server = new ApolloServer({
  typeDefs: importSchema('./graphql/schema.graphql'),
  resolvers,
  context: async ({ req }) => {
    return {
      db,
      authUser: req ? req.authUser : null
    };
  }
});

const app = express();
server.applyMiddleware({ app });

app.listen(config.server.port, () => {
  logger.info(
    `🚀 Server ready at http://localhost:${config.server.port}${
      server.graphqlPath
    }`
  );
});
