const express = require('express');
const bodyParser = require('body-parser');
const { ApolloServer, gql } = require('apollo-server-express');
const db = require('./models');
const schema = require('./graphql/schema');
const resolvers = require('./graphql/resolvers');
const env = process.env.NODE_ENV || 'development';
const config = require('./config');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Graphql endpoint
const server = new ApolloServer({
  secret: config.auth.jwtSecret,
  typeDefs: gql(schema),
  resolvers,
	context: ({ req }) => {
    authUser: req.user
  }
});

server.applyMiddleware({ app });

app.listen(4000, () => {
  console.log('Listening on port:4000');
});
