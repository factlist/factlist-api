const
    bcrypt = require('bcryptjs'),
    {pick} = require('lodash'),
    jwt = require('lib/jsonwebtoken'),
    {JWT_SECRET, JWT_LIFETIME} = process.env


module.exports = app => ({
    method: 'POST',
    path: '/access-tokens',
    schema: {
        tags: ['auth'],
        summary: 'Standard login',
        body: {
            type: 'object',
            required: ['email', 'password'],
            properties: {
                email: {type: 'string'},
                password: {type: 'string'},
            },
        },
        response: {
            200: {
                type: 'object',
                properties: {
                    token: {type: 'string'},
                },
            },
            401: {type: 'object'},
        },
    },
    handler: req =>
        app.db.users.findOne({email: req.body.email}, {
            fields: ['id', 'email', 'password', 'name'],
        })
            .then(userRecord =>
                userRecord || Promise.reject({statusCode: 401})
            )
            .then(userRecord =>
                bcrypt.compare(req.body.password, userRecord.password)
                    .then(match =>
                        !match
                            ? Promise.reject({statusCode: 401})
                            : jwt.sign(
                                pick(userRecord, ['id', 'email', 'name']),
                                JWT_SECRET,
                                {expiresIn: JWT_LIFETIME}
                            )
                    )
            )
            .then(token => ({
                token,
            }))
})
