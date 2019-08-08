const package = require('../package.json')


module.exports = {
    fastifySwagger: {
        routePrefix: '/documentation',
        exposeRoute: true,
        swagger: {
            info: {
                title: 'Factlist API Docs',
                version: package.version,
            },
            consumes: ['application/json'],
            produces: ['application/json'],
            securityDefinitions: {
                apiKey: {
                    type: 'apiKey',
                    in: 'header',
                    name: 'Authorization',
                }
            },
        }
    }
}
