module.exports = {
    tags: async link => {
      return await link.getTags();
    }
};
