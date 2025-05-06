-- 1. Drop the old users table if it exists
DROP TABLE IF EXISTS users;

-- 2. Create the users table
CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)   NOT NULL UNIQUE,
    first_name  VARCHAR(50)   NOT NULL,
    last_name   VARCHAR(50)   NOT NULL,
    email       VARCHAR(255)  NOT NULL UNIQUE,
    created_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Drop the old books table if it exists
DROP TABLE IF EXISTS books;

-- 4. Create the books table
CREATE TABLE books (
        id             INT AUTO_INCREMENT PRIMARY KEY,
        title          VARCHAR(255)   NOT NULL,
        author         VARCHAR(255),
        published_date DATE            NULL,
        genre          VARCHAR(50)    NULL,        -- e.g. "Literary Fiction", "Sci-Fi", "Nonfiction"
        created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at     TIMESTAMP       NULL ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT uq_books_title_author
        UNIQUE (title, author)
);

-- 5. Drop the reviews table if it exists
DROP TABLE IF EXISTS reviews;

-- 6. Create the reviews table
CREATE TABLE reviews (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    book_id       INT NOT NULL,
    user_id       INT NULL,
    review_title  VARCHAR(255) NOT NULL,
    review_text   TEXT NOT NULL,
    review_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating        TINYINT NULL,
    review_number INT NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_book
        FOREIGN KEY (book_id)
        REFERENCES books(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);