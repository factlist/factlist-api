const bcrypt = require('bcryptjs')


module.exports = app => ({
    method: 'POST',
    path: '/users',
    schema: {
        summary: 'Registration',
        body: {
            type: 'object',
            required: ['email', 'password'],
            properties: {
                email: {type: 'string'},
                password: {type: 'string'},
            },
        },
        response: {
            201: {
                type: 'object',
                properties: {
                    id: {type: 'number'},
                },
            },
            403: {
                type: 'object',
                properties: {
                    errors: {type: 'object'},
                },
            },
        },
    },
    handler: (req, res) =>
        app.db.users.findOne({email: req.body.email})
            .then(userRecord =>
                userRecord && Promise.reject({
                    statusCode: 403,
                    message: 'duplicate email',
                })
            )
            .then(() =>
                bcrypt.hash(req.body.password, 10)
            )
            .then(hashedPassword =>
                app.db.users.insert({
                    email: req.body.email,
                    password: hashedPassword,
                }, {
                    fields: ['id'],
                })
            )
            .then(({id}) => {
                res.status(201)
                return {id}
            }),
})
