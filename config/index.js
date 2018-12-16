const env = process.env.NODE_ENV || 'development';
const locale = require('./locales/en');

const config = {
  development: {
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
    auth: {
      tokenLifeTime: '1h',
			jwtSecret: 'secretKey',
			mailgunApiKey: process.env.mailgunApiKey,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL:
          'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.consumerKey,
        consumerSecret: process.env.consumerSecret,
        callbackURL: process.env.callbackURL
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
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.mailgunApiKey,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL:
          'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.consumerKey,
        consumerSecret: process.env.consumerSecret,
        callbackURL: process.env.callbackURL
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
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.mailgunApiKey,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL:
          'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.consumerKey,
        consumerSecret: process.env.consumerSecret,
        callbackURL: process.env.callbackURL
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
    auth: {
      tokenLifeTime: '1h',
      jwtSecret: 'secretKey',
      mailgunApiKey: process.env.mailgunApiKey,
      mailgunAccountEmail: 'http://factlist.com',
      mailgunDomain: 'account@factlist.com',
      twitter: {
        userProfileURL:
          'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
        consumerKey: process.env.consumerKey,
        consumerSecret: process.env.consumerSecret,
        callbackURL: process.env.callbackURL
      }
    }
  },
  logLevel: 'error'
};

module.exports = config[env];
