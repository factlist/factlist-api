const bcrypt = require('bcryptjs')


module.exports = app => ({
    method: 'POST',
    path: '/reset-password',
    schema: {
        tags: ['auth'],
        body:  {
            type: 'object',
            required: ['token', 'password'],
            properties: {
                token: {type: 'string'},
                password: {type: 'string'},
            },
        },
    },
    handler: req =>
        app.db.password_reset_requests.findOne({
            token: req.body.token,
            'expires_at >': new Date(),
        }, {
            fields: ['user_id'],
        })
            .then(pwResetReq =>
                pwResetReq || Promise.reject({statusCode: 401})
            )
            .then(({user_id}) =>
                bcrypt.hash(req.body.password, 10)
                    .then(hashedPassword =>
                        app.db.users.update({id: user_id}, {
                            password: hashedPassword,
                        })
                    )
                    .then(() =>
                        app.db.password_reset_requests.destroy({user_id})
                    )
            )
            .then(() => ({})),
})
