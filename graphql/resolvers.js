const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models').users;
const Topic = require('../models').topics;
const Tag = require('../models').tags;
const Link = require('../models').links;
const config = require('../config');

// Define resolvers
const resolvers = {
  Query: {
    // Fetch all users
    async users() {
      return await User.all();
    },

    // Get a user by it ID
    async user(_, { id }) {
      return await User.findByPk(id);
    },

    // Fetch all topics
    async topics() {
      return await Topic.all();
    },

    // Get a topic by it ID
    async topic(_, { id }) {
      return await Topic.findByPk(id);
    },

    // Fetch all tags
    async tags(_, args, { user }) {
      return await Tag.all();
    },

    // Get a tag by it ID
    async tag(_, { id }) {
      return await Tag.findByPk(id);
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
      return await jwt.sign(
        {
          sub: user.id
        },
        config.auth.jwtSecret
      );
    },
    // Create new user
    async createUser(_, { name, username, email, password }) {
      return await User.create({
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
      const user = await User.findByPk(id);

      // Update the user
      await user.update({
        name,
        username,
        email,
        password: await bcrypt.hash(password, 10)
      });

      return user;
    },

    //create topic
    async createTopic(_, { title, links }, { authUser }) {
			//Make sure user is logged in
      if (!authUser) {
        throw new Error('You must log in to continue!');
      }
      const data = {
        title,
        user_id: authUser.id,
        links
      };
      return await Topic.create(data, {
        include: [
          {
            model: Link,
            include: [{ model: Tag }]
          }
        ]
      });
    }
  }
};

module.exports = resolvers;
