BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS course_categories;
DROP TABLE IF EXISTS subscribers;

CREATE TABLE users
(
    id         INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    last_name  VARCHAR(32) NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    email      VARCHAR(32) UNIQUE,
    type       VARCHAR(32) NOT NULL
);
INSERT INTO users (last_name, first_name, email, type)
VALUES ('Ivanov', 'Ivan', 'ivanov@gmail.com', 'student'),
       ('Petrov', 'Petr', 'petrov@gmail.com', 'student');

CREATE TABLE courses
(
    id    INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  VARCHAR(64)  NOT NULL UNIQUE,
    title VARCHAR(128) NOT NULL,
    text  TEXT         NOT NULL,
    links TEXT,
    type  VARCHAR(64)  NOT NULL
);
INSERT INTO courses (name, title, text, links, type)
VALUES ('Python', 'TestTitle', 'TestText', NULL, 'offline'),
       ('SQL', 'TestTitle2', 'TestText', NULL, 'online'),
       ('Django', 'TestTitle3', 'TestText', NULL, 'online');

CREATE TABLE categories
(
    id   INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name VARCHAR(64) NOT NULL UNIQUE
);
INSERT INTO categories (name)
VALUES ('Python'),
       ('SQL');

CREATE TABLE course_categories
(
    course_id   INTEGER NOT NULL REFERENCES courses ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories ON DELETE CASCADE
);
INSERT INTO course_categories (course_id, category_id)
VALUES (1, 1),
       (2, 2),
       (3, 1),
       (3, 2);

CREATE TABLE subscribers
(
    user_id   INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses ON DELETE CASCADE
);
INSERT INTO subscribers (user_id, course_id)
VALUES (1, 1),
       (2, 2),
       (1, 3),
       (2, 3);

COMMIT TRANSACTION;
