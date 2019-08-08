insert into users (name, username, email, password) values
    ('Jon Snow', 'jon', 'king@nor.th', '$2a$10$Td8Cpo2dpAk/X2O06FDrg.oEkFpMHCtgcHTP9CZBDy7.CBqptYxvW'),
    ('Daenarys Targaryen', 'dany', 'kh@aale.si', '$2a$10$Td8Cpo2dpAk/X2O06FDrg.oEkFpMHCtgcHTP9CZBDy7.CBqptYxvW'),
    ('Tyrion Lannister', 'tyrion', 'imp@casterly.rock', '$2a$10$Td8Cpo2dpAk/X2O06FDrg.oEkFpMHCtgcHTP9CZBDy7.CBqptYxvW')
;
-- all password values above are hashes of the string "falanfilan"

insert into topics (user_id, title) values
    (1, 'winter'),
    (2, 'dragons'),
    (3, 'wine')
;

insert into links (topic_id, title, url, weight) values
    (1, 'Winter is coming', 'dummy.com', 0),
    (1, 'Stick them with the pointy end', 'dummy.com', 1),
    (2, 'I will take what is mine with fire and blood', 'dummy.com', 0),
    (2, 'All men must die', 'dummy.com', 1),
    (3, 'Never forget what you are', 'dummy.com', 0),
    (3, 'It''s not easy being drunk all the time', 'dummy.com', 1)
;

insert into tags (title) values
    ('foo'),
    ('bar')
;

insert into link_tags (link_id, tag_id) values
    (1, 1),
    (2, 2),
    (3, 1),
    (4, 2),
    (5, 1),
    (6, 1),
    (6, 2)
;
