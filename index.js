const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const { importSchema } = require('graphql-import');
const logger = require('./utils/logger');
const db = require('./models');
const config = require('./config');
const resolvers = require('./graphql/resolvers');
const auth = require('./middlewares/auth');

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
app.use(auth);
server.applyMiddleware({ app });

db.sequelize.sync().then(() => {
  app.listen(config.server.port, () => {
    logger.info(
      `🚀 Server ready at http://localhost:${config.server.port}${
        server.graphqlPath
      }`
    );
  });
});
