const bcrypt = require('bcryptjs')


module.exports = app => ({
    method: 'PATCH',
    path: '/users/:id',
    schema: {
        params: {
            id: {type: 'number'},
        },
        body: {
            type: 'object',
            additionalProperties: false,
            properties: {
                name: {type: 'string'},
                username: {type: 'string'},
                bio: {type: 'string'},
                avatar: {type: 'string'},
                password: {type: 'string'},
                password_confirmation: {
                    type: 'string',
                    const: {$data: '1/password'},
                },
            },
        },
    },
    handler: req => {
        if (req.user.id !== req.params.id)
            return Promise.reject({statusCode: 403})

        const {password, password_confirmation, ...attrs} = req.body

        return (
            !req.body.password
                ? Promise.resolve(attrs)
                : bcrypt.hash(password, 10)
                    .then(hashedPassword => ({
                        ...attrs,
                        password: hashedPassword,
                    }))
        )
            .then(attrs =>
                app.db.users.update(req.user.id, attrs, {
                    fields: ['id'],
                    single: true,
                })
            )
    },
})
