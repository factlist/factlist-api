// jsonwebtoken package promisified

const
    {promisify} = require('util'),
    jwt = require('jsonwebtoken')


module.exports = Object.assign({}, jwt, {
    sign: promisify(jwt.sign),
    decode: promisify(jwt.decode),
    verify: promisify(jwt.verify),
})
