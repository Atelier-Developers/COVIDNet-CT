USE aphrodite_feedbacks;

CREATE TABLE FEEDBACK
(
    id                     INT AUTO_INCREMENT NOT NULL,
    description            NVARCHAR(4096)       NOT NULL,
    analysis               NVARCHAR(4096)      NOT NULL,
    username               VARCHAR(50)        NOT NULL,
    created_time           DATETIME DEFAULT CURRENT_TIMESTAMP,
    image_path             VARCHAR(256)        NOT NULL,
    heatmap_path           VARCHAR(256)        NOT NULL,
    PRIMARY KEY (id)
);

