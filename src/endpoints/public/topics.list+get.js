const topicSchema = {
    type: 'object',
    properties: {
        id: {type: 'number'},
        title: {type: 'string'},
        username: {type: 'string'},
        links: {
            type: 'object',
            propertyNames: {type: 'number'},
            additionalProperties: {
                type: 'object',
                properties: {
                    id: {type: 'number'},
                    title: {type: 'string'},
                    url: {type: 'string'},
                    weight: {type: 'number'},
                    link_tags: {
                        type: 'object',
                        propertyNames: {type: 'number'},
                        additionalProperties: {
                            type: 'object',
                            properties: {
                                tag: {
                                    type: 'object',
                                    properties: {
                                        id: {type: 'number'},
                                        title: {type: 'string'},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

const fetchTopics = (db, criteria = {}, opts = {}) =>
    db.links_extended.find(criteria, {
        ...opts,
        decompose: {
            pk: 'topic_id',
            columns: {
                topic_id: 'id',
                topic_title: 'title',
                username: 'username',
            },
            links: {
                pk: 'id',
                columns: ['title', 'url', 'weight'],
                object: true,
                link_tags: {
                    pk: 'link_tag_id',
                    object: true,
                    tag: {
                        pk: 'tag_id',
                        columns: {
                            tag_id: 'id',
                            tag_title: 'title',
                        },
                    },
                },
            },
        },
    })

const listEndpoint = app => ({
    method: 'GET',
    path: '/topics',
    schema: {
        tags: ['topic'],
        response: {
            200: {
                type: 'array',
                items: topicSchema,
            },
        },
    },
    handler: () =>
        fetchTopics(app.db),
})

const showEndpoint = app => ({
    method: 'GET',
    path: '/topics/:id',
    schema: {
        tags: ['topic'],
        params: {
            id: {type: 'number'},
        },
        response: {
            200: topicSchema,
            404: {type: 'object'},
        },
    },
    handler: req =>
        fetchTopics(app.db, {
            topic_id: req.params.id,
        }, {
            single: true,
        })
            .then(topicRecord =>
                topicRecord || Promise.reject({statusCode: 404})
            ),
})

module.exports = [listEndpoint, showEndpoint]
