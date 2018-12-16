module.exports = (str, data) => {
  Object.keys(data).forEach(val => {
    str = str.replace(val, data[val]);
  });
  return str;
};
