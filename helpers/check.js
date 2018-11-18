const check = {
  Auth: authUser => {
    if (!authUser) {
      throw new Error('You are not authorized!');
    }
  }
};

module.exports = check;
