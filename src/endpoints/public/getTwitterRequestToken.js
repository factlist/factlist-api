module.exports = app => ({
    method: 'GET',
    path: '/get-twitter-request-token',
    schema: {
        tags: ['auth'],
        summary: 'Twitter OAuth',
        description: (
            'Request an OAuth request token from Twitter. More info on:\n' +
            'https://developer.twitter.com/en/docs/twitter-for-websites/log-in-with-twitter/guides/implementing-sign-in-with-twitter\n' +
            '<br />After obtaining this token clients should probably redirect to `https://twitter.com/oauth/authenticate?oauth_token={token}`'
        ),
        response: {
            200: {
                type: 'object',
                properties: {
                    reqToken: {type: 'string'},
                },
            },
            403: {type: 'object'},
        },
    },
    handler: () =>
        app.twitterOAuthCli.getOAuthRequestToken()
            .then(([reqToken]) => ({
                reqToken
            }))
})
