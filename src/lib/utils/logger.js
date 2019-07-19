const winston = require('winston');
const config = require('config');
winston.config.npm.levels;

const logger = winston.createLogger({
  levels: winston.config.syslog.levels,
  transports: [
    new winston.transports.Console({
      level: config.logLevel || 'info',
      showLevel: false
    })
  ]
});

module.exports = logger;
