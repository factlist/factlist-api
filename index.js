const express = require('express');
const session = require('express-session');
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
app.use(require('cookie-parser')());
app.use(bodyParser.json({ type: '*/*' }));
app.use(session({ secret: 'blah', name: 'id', cookie: { secure: false } }));
app.use('/graphql', requireAuth);
app.use(passport.initialize());
app.use(passport.session());

app.get('/auth/logout', (req, res) => {
  req.logout();
  res.redirect('/');
});

app.get('/test', (req, res) => {
  console.log(req.isAuthenticated());
  res.send('test');
});

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
