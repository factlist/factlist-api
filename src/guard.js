const
    jwt = require('lib/jsonwebtoken'),
    {JWT_SECRET} = process.env


module.exports = (req, res) => {
    const token = (req.headers.authorization || '').split(' ')[1]

    return jwt.verify(token, JWT_SECRET)
        .then(claims => {
            req.user = claims
        })
        .catch(() =>
            res.status(401).send({})
        )
}
