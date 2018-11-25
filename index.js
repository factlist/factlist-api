const express = require('express');
const passport = require('passport');
const bodyParser = require('body-parser');
const { ApolloServer } = require('apollo-server-express');
const { importSchema } = require('graphql-import');
const logger = require('./utils/logger');
const db = require('./models');
const config = require('./config');
const resolvers = require('./graphql/resolvers');
const authenticate = require('./auth');

const requireAuth = passport.authenticate('jwt', { session: false });
require('./services/passport');

const server = new ApolloServer({
  typeDefs: importSchema('./graphql/schema.graphql'),
  resolvers,
  context: async ({ req }) => {
    return {
      db,
      authUser: req ? req.user : null
    };
  }
});

const app = express();
app.use('/graphql', requireAuth);
app.use(bodyParser.json({ type: '*/*' }));

authenticate(app);
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
