const
    fs = require('fs'),
    url = require('url'),
    fastify = require('fastify'),
    fastifySwagger = require('fastify-swagger'),
    fastifyCors = require('fastify-cors'),
    massive = require('massive'),
    nodemailer = require('nodemailer'),
    {PromiseOAuth} = require('oauth-libre'),
    guard = require('./guard'),
    {mergeDeep} = require('./lib/util'),
    config = require('./config'),
    {env} = process


const main = () => {
    const app = fastify({logger: true})

    app.register(fastifySwagger, config.fastifySwagger)
    app.ready(() => app.swagger())

    app.register(fastifyCors, {origin: env.UI_URL})

    setupRouteGroup(app, __dirname + '/endpoints/public')

    app.register((app, opts, next) => {
        setupRouteGroup(app, __dirname + '/endpoints/protected', {
            security: [{'apiKey': []}],
        })
        app.addHook('onRequest', guard)
        next()
    })

    app.setErrorHandler(handleErrors(app))

    app.setNotFoundHandler((req, res) =>
        res.status(404).send({message: 'No such route!'})
    )

    app.decorate('twitterOAuthCli', makeTwitterOAuthCli())

    app.decorate('mailer', makeMailCli({logger: app.log}))

    makeDBCli()
        .then(db => {
            app.decorate('db', db)

            return app.listen({host: env.HOST, port: env.PORT})
        })
        .catch(err => {
            app.log.error(err)
            process.exit(1)
        })
}

// Register all routes in a given directory with the app
const setupRouteGroup = (app, targetDir, defaultSchema = {}) => {
    fs.readdirSync(targetDir)
        .forEach(filename =>
            [].concat( // to make sure the value is an array
                require(targetDir + '/' + filename)
            )
                .forEach(routeFactory =>
                    app.route(
                        mergeDeep(
                            {schema: defaultSchema},
                            routeFactory(app)
                        )
                    )
                )
        )
}

const handleErrors = app => (err, req, res) => {
    if (err.validation) {
        let i, valErrs = {}

        for (i in err.validation)
            if (err.validation[i].keyword === 'required')
                return res.status(400).send({})
            else
                valErrs[err.validation[i].dataPath] = err.validation[i].message

        return res.status(422).send(valErrs)
    }

    if (err.statusCode === 500 || !err.statusCode) {
        app.log.error(err)
        return res.status(500).send({message: 'we fucked up, sorry'})
    }

    return res.status(err.statusCode).send(err)
}

const makeTwitterOAuthCli = () =>
    new PromiseOAuth(
        'https://api.twitter.com/oauth/request_token',
        'https://api.twitter.com/oauth/access_token',
        env.TWITTER_CONSUMER_KEY,
        env.TWITTER_CONSUMER_SECRET,
        '1.0',
        env.UI_URL + env.TWITTER_CALLBACK_PATH,
        'HMAC-SHA1'
    )

// @returns Promise
const makeDBCli = () => {
    const
        {hostname: host, port, auth, pathname} = url.parse(env.DB_URL),
        [user, password] = auth.split(':'),
        database = pathname.slice(1), // ditch the leading slash
        poolSize = env.DB_POOLSIZE

    return massive({host, port, database, user, password, poolSize})
}

const makeMailCli = ({logger}) =>
    nodemailer.createTransport({
        host: env.SMTP_HOST,
        port: env.SMTP_PORT,
        secure: env.SMTP_SECURE !== 'false',
        auth: {
            user: env.SMTP_USER,
            pass: env.SMTP_PASSWORD,
        },
        authMethod: env.SMTP_AUTHMETHOD,
        logger,
    }, {
        from: `Factlist <${env.SMTP_FROM}>`,
    })

main()
