module.exports = {
    topics: async user => {
      return await user.getTopics();
    }
};
