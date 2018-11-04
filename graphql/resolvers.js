const { users, topics, tags } = require('../models');

// Define resolvers
const resolvers = {
  Query: {
    // Fetch all users
    async users() {
      return await users.all();
    },

    // Get a user by it ID
    async user(_, { id }) {
      return await users.findById(id);
    },

    // Fetch all topics
    async topics() {
      return await topics.all();
    },

    // Get a topic by it ID
    async topic(_, { id }) {
      return await topics.findById(id);
    },

    // Fetch all tags
    async tags(_, args, { user }) {
      return await tags.all();
    },

    // Get a tag by it ID
    async tag(_, { id }) {
      return await tags.findById(id);
    }
  },

  User: {
    // Fetch all topics created by a user
    async topics(user) {
      return await user.getTopics();
    }
  },
  Topic: {
    // Fetch all links created by a topic
    async links(topic) {
      return await topic.getLinks();
    }
  },
  Link: {
    // Fetch all tags created by a link
    async tags(link) {
      return await link.getTags();
    }
  }
};

module.exports = resolvers;
