CREATE DATABASE IF NOT EXISTS disaster_db;

USE disaster_db;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  google_id VARCHAR(255) DEFAULT NULL,
  name VARCHAR(255) DEFAULT NULL,
  email VARCHAR(255) DEFAULT NULL,
  profile_pic TEXT,
  PRIMARY KEY (id),
  UNIQUE KEY google_id (google_id),
  UNIQUE KEY email (email)
);

CREATE TABLE disaster_uploads (
    image_id INT NOT NULL AUTO_INCREMENT,
    user_id INT DEFAULT NULL,
    image_path VARCHAR(255) DEFAULT NULL,
    disaster_type VARCHAR(50) DEFAULT NULL,
    latitude DECIMAL(10,8) DEFAULT NULL,
    longitude DECIMAL(11,8) DEFAULT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255) DEFAULT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Unverified',
    PRIMARY KEY (image_id),
    KEY user_id (user_id),
    CONSTRAINT disaster_uploads FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE reactions (
    user_id INT DEFAULT NULL,
    card_id INT DEFAULT NULL,
    reaction VARCHAR(50) DEFAULT NULL,
    suggested_type VARCHAR(50) DEFAULT NULL,
    reported VARCHAR(50) DEFAULT NULL,
    UNIQUE KEY (user_id, card_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (card_id) REFERENCES disaster_uploads(image_id)
);