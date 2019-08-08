const {omit} = require('lodash')


const exampleBody = `
    {
      "title": "carrot",
      "links": {
        "*7482-2422": {
          "url": "loremipsum.com",
          "link_tags": {
            "*8439-3379": {
              "tag": {
                "id": "*2849-8646",
                "title": "baz"
              }
            }
          }
        },
        "*3844-8923": {
          "title": "Love me two times baby",
          "url": "peoplearestrange.com",
          "weight": 0,
          "link_tags": {
            "*2213-3296": {
              "tag": {
                "id": 1,
                "title": "foo"
              }
            }
          }
        }
      }
    }
`

const description = `
NOTE: The expected body of this endpoint unfortunately cannot be automatically
displayed by Swagger UI as it does not support the JSON Schema features we rely
on here.

So below is an example we prepared manually:

<br /><br />\n${exampleBody}<br />

The random id values starting with "*" denote that the relevant record will be
created.

Check out the JSON Merge Patch standard (RFC 7396) for more about this kind of
payload. We are using that format in both the create and the update endpoints.
`

const bodySchema = {
    type: 'object',
    additionalProperties: false,
    properties: {
        title: {type: 'string'},
        links: {
            type: 'object',
            propertyNames: {type: ['number', 'string']},
            additionalProperties: {
                type: ['object', 'null'],
                properties: {
                    title: {type: 'string'},
                    url: {type: 'string'},
                    weight: {type: 'number'},
                    link_tags: {
                        type: 'object',
                        propertyNames: {type: ['number', 'string']},
                        additionalProperties: {
                            type: ['object', 'null'],
                            properties: {
                                tag: {
                                    type: 'object',
                                    properties: {
                                        id: {type: ['number','string']},
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

const patchTopic = (tx, topicId, patch) => {
    const {links = {}, ...topicAttrs} = patch

    return Promise.all([
        Object.keys(topicAttrs).length
            ? tx.topics.update({id: topicId}, topicAttrs, {
                fields: ['id'],
            })
            : Promise.resolve({id: topicId}),

        ...Object.entries(links).map(([linkId, linkPatch]) => {
            const {link_tags = {}, ...linkAttrs} = linkPatch || {}

            if (linkPatch === null)
                return tx.links.destroy({id: linkId})

            return (
                linkId[0] === '*'
                    ? tx.links.insert({topic_id: topicId, ...linkAttrs})
                    : tx.links.update({id: linkId}, linkAttrs, {single: true})
            )
                .then(({id: linkId}) =>
                    Promise.all(
                        Object.entries(link_tags).map(([ltId, ltPatch]) => {
                            if (ltPatch === null)
                                return tx.link_tags.destroy({id: ltId})

                            return (
                                ltPatch.tag.id[0] === '*'
                                    ? tx.tags.insert(omit(ltPatch.tag, ['id']))
                                    : Promise.resolve({id: ltPatch.tag.id})
                            )
                                .then(tagRecord =>
                                    tx.link_tags.insert({
                                        link_id: linkId,
                                        tag_id: tagRecord.id,
                                    })
                                )
                        })
                    )
                )
        }),
    ])
}

const createEndpoint = app => ({
    method: 'POST',
    path: '/topics',
    schema: {
        tags: ['topic'],
        description,
        body: bodySchema,
        response: {
            201: {
                type: 'object',
                properties: {
                    id: {type: 'string'},
                },
            },
        },
    },
    handler: (req, res) =>
        app.db.withTransaction(tx =>
            tx.topics.insert({
                user_id: req.user.id,
            }, {
                fields: ['id'],
            })
                .then(topicRecord =>
                    patchTopic(tx, topicRecord.id, req.body)
                )
        )
            .then(([{id}]) => {
                res.status(201)
                return {id}
            }),
})

const patchEndpoint = app => ({
    method: 'PATCH',
    path: '/topics/:id',
    schema: {
        tags: ['topic'],
        description,
        // consumes: ['application/merge-patch+json'], // TODO
        params: {
            id: {type: 'number'},
        },
        body: bodySchema,
        response: {
            200: {
                type: 'object',
                properties: {
                    id: {type: 'string'},
                },
            },
            403: {type: 'object'},
            404: {type: 'object'},
        },
    },
    handler: req =>
        app.db.topics.findOne(req.params.id, {
            fields: ['user_id'],
        })
            .then(topicRecord =>
                topicRecord || Promise.reject({statusCode: 404})
            )
            .then(({user_id}) =>
                user_id === req.user.id || Promise.reject({statusCode: 403})
            )
            .then(() =>
                app.db.withTransaction(tx =>
                    patchTopic(tx, req.params.id, req.body)
                )
            )
            .then(() => ({
                id: req.params.id,
            })),
})

module.exports = [createEndpoint, patchEndpoint]
