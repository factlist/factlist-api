create table users (
  id serial primary key,
  name text,
  username text unique,
  twitterid bigint unique,
  email text unique,
  password text
);

create table password_reset_requests (
    user_id int not null references users (id) on delete cascade,
    token text not null,
    expires_at timestamptz not null
);

create table topics (
  id serial primary key,
  user_id int not null references users (id),
  title text
);

create table links (
  id serial primary key,
  topic_id int not null references topics (id) on delete cascade,
  title text,
  url text,
  weight int
);

create table tags (
  id serial primary key,
  title text unique
);

create table link_tags (
  id serial primary key,
  link_id int not null references links (id) on delete cascade,
  tag_id int not null references tags (id),
  unique (link_id, tag_id)
);

create view links_extended as
    select
        l.id,
        l.title,
        l.url,
        l.weight,
        t.id topic_id,
        t.title topic_title,
        t.user_id,
        u.username,
        ltg.id link_tag_id,
        tg.id tag_id,
        tg.title tag_title
    from
        links l
        join topics t on t.id = l.topic_id
        join users u on u.id = t.user_id
        join link_tags ltg on ltg.link_id = l.id
        join tags tg on tg.id = ltg.tag_id
;
