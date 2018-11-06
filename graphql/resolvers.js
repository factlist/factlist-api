const bcrypt = require('bcryptjs');
const config = require('../config');
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
  },
  Mutation: {
    // Handles user login
    async login(_, { email, password }) {
      const user = await User.find({ where: { email } });

      if (!user) {
        throw new Error('No user with that email');
      }

      const valid = await bcrypt.compare(password, user.password);

      if (!valid) {
        throw new Error('Incorrect password');
      }
      // Return json web token
      return jwt.sign(
        { id: user.id, email: user.email },
        	config.auth.jwtSecret,
        { expiresIn: '1y' }
      );
    },
    // Create new user
    async createUser(_, { name, username, email, password }) {
      return await users.create({
        name,
        username,
        email,
        password: await bcrypt.hash(password, 10)
      });
    },

    // Update a particular user
    async updateUser(_, { id, name, username, email, password }, { authUser }) {
      // Make sure user is logged in
      if (!authUser) {
        throw new Error('You must log in to continue!');
      }

      // fetch the user by it ID
      const user = await users.findById(id);

      // Update the user
      await user.update({
        name,
        username,
        email,
        password: await bcrypt.hash(password, 10)
      });

      return user;
    }
  }
};

module.exports = resolvers;
