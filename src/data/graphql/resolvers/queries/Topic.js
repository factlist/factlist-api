module.exports = {
    links: async topic => {
      return await topic.getLinks();
    }
};
