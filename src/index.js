const path = require('path')
const express = require('express');
const session = require('express-session');
const passport = require('passport');
const bodyParser = require('body-parser');
const cors = require('cors');
const { ApolloServer } = require('apollo-server-express');
const { importSchema } = require('graphql-import');
const logger = require('./lib/utils/logger');
const db = require('./data/models');
const config = require('./config');
const resolvers = require('./data/graphql/resolvers');
const authenticate = require('./endpoints/auth');

const requireAuth = passport.authenticate('jwt', { session: false });
require('./lib/services/passport');

const server = new ApolloServer({
  typeDefs: importSchema(path.join(__dirname, './data/graphql/schema.graphql')),
  resolvers,
  context: async ({ req }) => {
    return {
      db,
      authUser: req ? req.user : null
    };
  }
});

const app = express();
app.use(cors())
app.use(require('cookie-parser')());
app.use(bodyParser.json({ type: '*/*' }));
app.use(session({ secret: 'blah', name: 'id', cookie: { secure: false } }));
app.use('/api/v1/graphql', requireAuth);
app.use(passport.initialize());
app.use(passport.session());
/*
app.get('/api/v1/auth/logout', (req, res) => {
  req.logout();
  res.redirect('/');
});
*/
authenticate(app);
const graphqlPath = '/api/v1/graphql';
server.applyMiddleware({ app , path: graphqlPath });

db.sequelize.sync().then(() => {
  app.listen(config.server.port, () => {
    logger.info(
      `🚀 Server ready at http://localhost:${config.server.port}${
        server.graphqlPath
      }`
    );
  });
});
