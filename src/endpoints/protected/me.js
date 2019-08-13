module.exports = app => ({
    method: 'GET',
    path: '/me',
    schema: {
        response: {
            200: {
                type: 'object',
                properties: {
                    id: {type: 'number'},
                    name: {type: 'string'},
                    username: {type: 'string'},
                    twitterid: {type: 'string'},
                    email: {type: 'string'},
                    bio: {type: 'string'},
                    avatar: {type: 'string'},
                },
            },
        },
    },
    handler: req =>
        app.db.users.findOne(req.user.id, {
            fields: [
                'id', 'name', 'username', 'twitterid', 'email', 'bio', 'avatar',
            ],
        }),
})
