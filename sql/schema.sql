DROP TABLE IF EXISTS reports;

CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    patientId TEXT NOT NULL,
    content TEXT NOT NULL,
    originalImage TEXT NOT NULL,
    resultImage TEXT NOT NULL
);