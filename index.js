const express = require('express');
const bodyParser = require('body-parser');
const { ApolloServer, gql } = require('apollo-server-express');

const schema = require('./graphql/schema/schema');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Graphql endpoint
const server = new ApolloServer({
  typeDefs: gql(schema),
});

server.applyMiddleware({ app });


app.listen(4000, () => {
  console.log('Listening on port:4000');
});
