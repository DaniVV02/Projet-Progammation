CREATE TABLE IF NOT EXISTS question_db (
    id_question INTEGER PRIMARY KEY AUTOINCREMENT,
    text_question TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tag_db (
    id_tag INTEGER PRIMARY KEY AUTOINCREMENT,
    text_tag TEXT NOT NULL,
    id_question INTEGER NOT NULL,
    FOREIGN KEY (id_question) REFERENCES question_db(id_question)
);

CREATE TABLE qcm (
    id_qcm INTEGER PRIMARY KEY,
    etiquette TEXT NOT NULL,
    question TEXT NOT NULL,
    choix_1 TEXT NOT NULL,
    choix_2 TEXT NOT NULL,
    choix_3 TEXT NOT NULL,
    choix_4 TEXT NOT NULL,
    reponse TEXT NOT NULL
);