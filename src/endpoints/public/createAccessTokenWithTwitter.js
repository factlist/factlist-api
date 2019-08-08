const
    {pick} = require('lodash'),
    jwt = require('lib/jsonwebtoken'),
    {JWT_SECRET, JWT_LIFETIME} = process.env


const twitterVerifyEndpoint =
    'https://api.twitter.com/1.1/account/verify_credentials.json' +
    '?include_email=true'

module.exports = app => ({
    method: 'GET',
    path: '/create-access-token-with-twitter',
    schema: {
        tags: ['auth'],
        summary: 'Twitter OAuth',
        description: (
            'Twitter OAuth callback endpoint. More info on:\n' +
            'https://developer.twitter.com/en/docs/twitter-for-websites/log-in-with-twitter/guides/implementing-sign-in-with-twitter'
        ),
        query: {
            oauth_token: {type: 'string'},
            oauth_verifier: {type: 'string'},
        },
    },
    handler: req =>
        app.twitterOAuthCli.getOAuthAccessToken(
            req.query.oauth_token,
            null,
            req.query.oauth_verifier
        )
            .then(([accToken, accTokenSecret]) =>
                app.twitterOAuthCli.get(
                    twitterVerifyEndpoint,
                    accToken,
                    accTokenSecret
                )
            )
            .then(([twitterUserDataRaw]) =>
                JSON.parse(twitterUserDataRaw)
            )
            .then(({id, email, name, screen_name}) =>
                app.db.users.insert({
                    twitterid: id,
                    username: screen_name,
                    email,
                    name,
                }, {
                    onConflictUpdate: ['twitterid'],
                    onConflictUpdateExclude: ['username'],
                    fields: ['id', 'name', 'email'],
                })
            )
            .then(userRecord =>
                jwt.sign(
                    pick(userRecord, ['id', 'email', 'name']),
                    JWT_SECRET,
                    {expiresIn: JWT_LIFETIME}
                ),
            )
            .then(token => ({
                token,
            })),
})
