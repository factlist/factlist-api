const env = process.env.NODE_ENV || 'development';
const locale = require('./locales/en');

const config = {
  development: {
    locale,
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    logging: false,
    database: process.env.DB_NAME,
    host: process.env.DB_HOST,
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    auth: {
      tokenLifeTime: '30d',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.MAILGUN_API_KEY,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL:
          'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.TWITTER_CONSUMER_KEY,
        consumerSecret: process.env.TWITTER_CONSUMER_SECRET,
        callbackURL: process.env.TWITTER_CALLBACK_URL
      }
    },
    service: {
      embedly: {
        api: 'https://api.embedly.com/1/oembed',
        key: process.env.EMBEDLY_API_KEY
      }
    },
    logLevel: 'debug'
  },

  docker: {
    locale,
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    logging: false,
    database: process.env.DB_NAME,
    host: process.env.DB_HOST,
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    embedly: {
      api: 'https://api.embedly.com/1/oembed',
      key: process.env.EMBEDLY_API_KEY
    },
    auth: {
      tokenLifeTime: '30d',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.MAILGUN_API_KEY,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL: 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.TWITTER_CONSUMER_KEY,
        consumerSecret: process.env.TWITTER_CONSUMER_SECRET,
        callbackURL: process.env.TWITTER_CALLBACK_URL
      }
    }
  },

  test: {
    locale,
    username: 'root',
    password: '',
    logging: false,
    database: 'factlist-api',
    host: 'localhost',
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    embedly: {
      api: 'https://api.embedly.com/1/oembed',
      key: process.env.EMBEDLY_API_KEY
    },
    auth: {
      tokenLifeTime: '30d',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.MAILGUN_API_KEY,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL: 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.TWITTER_CONSUMER_KEY,
        consumerSecret: process.env.TWITTER_CONSUMER_SECRET,
        callbackURL: process.env.TWITTER_CALLBACK_URL
      }
    },
    logLevel: 'info'
  },

  production: {
    locale,
    username: 'root',
    password: '',
    logging: false,
    database: 'factlist-api',
    host: process.env.DB_HOST,
    dialect: 'mysql',
    timezone: '+00:00',
    define: {
      paranoid: true,
      timestamps: true,
      freezeTableName: true,
      underscored: true
    },
    server: {
      port: process.env.port || 4000
    },
    embedly: {
      api: 'https://api.embedly.com/1/oembed',
      key: process.env.EMBEDLY_API_KEY
    },
    auth: {
      tokenLifeTime: '30d',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.MAILGUN_API_KEY,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL:'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.TWITTER_CONSUMER_KEY,
        consumerSecret: process.env.TWITTER_CONSUMER_SECRET,
        callbackURL: process.env.TWITTER_CALLBACK_URL
      }
    }
  },
  logLevel: 'error'
};

module.exports = config[env];
