<p align="center">
  <h1 align="center">Factlist</h1>

  <p align="center">
    <a href="http://factlist.com" target="_blank">
      <img width="150" src="https://avatars2.githubusercontent.com/u/33418877?s=200&v=4" />
    </a>
  </p>
</p>

## Setup

### Dependencies

- Node v8+

- NPM v6+

- Postgres v10+

- Migra

        pip install --user migra[pg]

- jq (Development dependency for readable development logs)

- NPM dependencies

        npm i

### Environment

Copy the `.env.example` file to `.env` and modify as necessary.


### Database

- Create the user, the database, and the helper database. Make
  sure the new user is the owner of the public schema of the
  helper database.

  Exact commands depend on the Postgres installation and the
  environment. Here are example commands that would work for a
  Postgres superuser:

        createuser factlist
        createdb factlist -O factlist
        createdb factlist_next -O factlist
        psql factlist_next -c 'alter schema public owner to factlist'

- Migrate the database. See the migration section below.

- Optionally seed the database:

        npm run db:seed


## Database Migrations

- Edit the database schema file (Skip this if first time migrating)

- Generate a migration script:

        npm run db:diff

- Review the generated script, modify as necessary, then apply:

        npm run db:patch

- See [Migra][1] and [state driven database delivery][2] for more
  information on this kind of approach to migrations.


### API Documentation

Documentation is powered by the Fastify Swagger plugin which
automatically generates an OpenAPI v2 specification from the
app's route declarations.

To see the docs go to `http://$HOST:$PORT/documentation` in your
browser when the server is running.


### Development

- Start the server:

        npm start


### Gotchas

- After adding a new route or modifying the schema of a route;
  Fastify Swagger sometimes causes the server to crash, and it
  can't recover despite Nodemon. Just kill the Nodemon process and
  start it again in that case.


### Deployment

TODO


[1]: https://djrobstep.com/docs/migra
[2]: https://google.com/#q=state+driven+database+delivery
