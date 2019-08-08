module.exports = app => ({
    method: 'DELETE',
    path: '/topics/:id',
    schema: {
        tags: ['topic'],
        params: {
            id: {type: 'number'},
        },
        response: {
            200: {
                type: 'object',
                properties: {
                    id: {type: 'string'},
                },
            },
            404: {type: 'object'},
        },
    },
    handler: req =>
        app.db.topics.destroy({
            id: req.params.id,
            user_id: req.user.id,
        }, {
            fields: ['user_id'],
        })
            .then(topicRecord =>
                topicRecord || Promise.reject({statusCode: 404})
            )
            .then(() => ({
                id: req.params.id,
            })),
})
