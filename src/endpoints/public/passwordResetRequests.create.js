const
    bcrypt = require('bcryptjs'),
    {UI_URL, PASSWORD_RESET_CALLBACK_PATH} = process.env


module.exports = app => ({
    method: 'POST',
    path: '/password-reset-requests',
    schema: {
        tags: ['auth'],
        body: {
            type: 'object',
            required: ['email'],
            properties: {
                email: {type: 'string'},
            },
        },
        response: {
            201: {type: 'object'},
        },
    },
    handler: (req, res) =>
        app.db.users.findOne({email: req.body.email})
            .then(userRecord =>
                userRecord || Promise.reject({statusCode: 201})
                // Returning 201 to make it look like the operation succeeded,
                // as a security precaution, to prevent leaking information
                // regarding the mail's existence.

            )
            .then(userRecord =>
                bcrypt.hash(String(new Date()), 5)
                    .then(token =>
                        app.db.password_reset_requests.insert({
                            user_id: userRecord.id,
                            token,
                            expires_at:
                                new Date(new Date().getTime() + 60*60*1000),
                        }, {
                            fields: ['token'],
                        })
                    )
                    .then(({token}) =>
                        app.mailer.sendMail({
                            to: `${userRecord.name} <${userRecord.email}>`,
                            subject: 'Here is your password reset link',
                            text: (
                                UI_URL +
                                PASSWORD_RESET_CALLBACK_PATH +
                                '?token=' + token
                            ),
                        })
                    )
            )
            .then(() => {
                res.status(201)
                return {}
            }),
})
