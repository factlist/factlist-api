const urllib = require('url')
const http = require('http')
const https = require('https')
const htmlparser2 = require('htmlparser2')


module.exports = () => ({
    method: 'POST',
    path: '/get-site-title',
    schema: {
        description: 'Get the title of the given site as quickly as possible.',
        body: {
            type: 'object',
            properties: {
                url: {type: 'string'},
            },
        },
        response: {
            200: {
                type: 'object',
                properties: {
                    title: {type: 'string'},
                },
            },
            400: {type: 'object'},
        },
    },
    handler: req =>
        request(req.body.url)
            .catch(err =>
                Promise.reject({
                    statusCode: err.code === 1 ? 400 : 500,
                })
            )
            .then(streamParseTitle)
            .then(title => ({
                title,
            })),
})

const adapters = {'http:': http, 'https:': https}

const request = url =>
    new Promise((resolve, reject) => {
        const protocol = urllib.parse(url).protocol
        const adapter = adapters[protocol]

        if (!adapter)  // bad protocol value
            return reject({code: 1})

        const req = adapter.request(url, res => {
            const statusType = String(res.statusCode)[0]

            return statusType === '3' ? resolve(request(res.headers.location)) :
                   statusType === '2' ? resolve(res) :
                                        reject({code: 2, response: res})
        })

        req.on('error', err => reject({code: 3, error: err}))

        req.end()
    })

const streamParseTitle = response =>
    new Promise((resolve, reject) => {
        const parser = makeStreamTitleParser(title => {
            resolve(title)
            response.destroy()
        })

        response.pipe(parser)

        parser.end()
    })

const makeStreamTitleParser = (onFinish = () => {}) =>
    new htmlparser2.Parser({
        inTitleTag: false,
        titleText: null,

        onopentag(tagname, attribs) {
            if (tagname === 'title')
                this.inTitleTag = true
        },

        ontext(text) {
            if (this.inTitleTag)
                this.titleText = text
        },

        onclosetag(tagname) {
            if (tagname === 'title')
                onFinish(this.titleText)
        },
    }, {
        decodeEntities: true,
    })
