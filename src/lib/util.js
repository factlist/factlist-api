const {mergeWith, isArray, concat} = require('lodash')


// Recursive merge with array concatenation
const mergeDeep = (a, b) =>
    mergeWith({}, a, b, (c, d) =>
        (isArray(c) && isArray(d))
            ? c.concat(d)
            : undefined
    )

module.exports = {
    mergeDeep,
}
