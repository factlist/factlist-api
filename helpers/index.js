const check = require('./check');
const token = require('./token');
const getUserFromTag = require('./get-user-from-tag');
const getUserFromLink = require('./get-user-from-link');
const attrReplacer = require('./locale-attr-replacer');

module.exports = {
  check,
  token,
  getUserFromTag,
  getUserFromLink,
  attrReplacer
};
