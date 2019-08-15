module.exports = app => ({
  method: 'GET',
  path: '/tags',
  schema: {
    query: {
      search: {type: 'string'},
    },
  },
  handler: req =>
    req.query.search
      ? app.db.tags.where(
        "title ILIKE '%' || $1 || '%'",
        [req.query.search],
        {
          fields: ['id', 'title'],
        }
      )
      : app.db.tags.find({}, {
        fields: ['id', 'title'],
      }),
})
