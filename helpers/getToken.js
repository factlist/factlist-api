module.exports = authorizationHeader => {
  const token = authorizationHeader || false;

  if (!token || token.split(' ')[0] !== 'Bearer')
    throw new Error('Invalid Authorization Header');

  return token.split(' ')[1];
};
