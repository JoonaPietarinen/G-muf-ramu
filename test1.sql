INSERT INTO areas (id, name, is_private) VALUES (100, 'testGeneral Discussion', FALSE);
INSERT INTO areas (id, name, is_private) VALUES (200, 'testBug Reports', FALSE);
INSERT INTO users (username, password, is_admin) VALUES ('testuser', 'password', FALSE);
INSERT INTO profiles (user_id, bio, profile_image) VALUES (1, 'This is a test bio.', '/static/images/profile.png');
INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin', TRUE);

