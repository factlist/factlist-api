<p align="center">
  <h1 align="center">Factlist</h1>

  <p align="center">
    <a href="http://factlist.com" target="_blank">
      <img width="150" src="https://avatars2.githubusercontent.com/u/33418877?s=200&v=4" />
    </a>
  </p>
</p>

## About

The Factlist API service is built with NodeJS, GraphQL and latest stable versions of other NPM packages.

## Setup

### Environment

The application expects the below environment variables to be
present. Please configure your environment properly before
proceeding to the next section:

    DB_USER
    DB_PASSWORD
    DB_NAME
    DB_HOST
    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET
    TWITTER_CALLBACK_URL
    MAILGUN_API_KEY
    EMBEDLY_API_KEY


### Dependencies

- Install Node V8+ and Mysql (MariaDB) preferably using the
  package manager of the host operating system.

- Install NPM modules: `yarn install`


### Database

- Run the database server, connect to it as super user, then make
    Factlist specific configuration:

        mysql> CREATE DATABASE factlist-api;
        mysql> CREATE USER factlist@localhost IDENTIFIED BY password;
        mysql> GRANT ALL PRIVILEGES ON `factlist-api`.* TO factlist@localhost;
        mysql> FLUSH PRIVILEGES;

- Migrate the database: `yarn db:migrate`

- Seed the database: `yarn db:seed`

### Development

- Start server watch: `yarn watch`
