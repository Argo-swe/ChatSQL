-- Tabella credenziali di login tecnico
CREATE TABLE IF NOT EXISTS admins (
  username TEXT PRIMARY KEY NOT NULL,
  password TEXT NOT NULL
);

-- Tabella dizionari dati 
CREATE TABLE IF NOT EXISTS dictionaries (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT UNIQUE NOT NULL,
  description TEXT
);

-- Aggiunta profili da tecnico

INSERT OR IGNORE INTO admins(username, password) VALUES ('admin', 'admin');


-- Aggiunta dizionari dati

INSERT OR IGNORE INTO dictionaries(name, description) VALUES ('orders', 'The orders database is designed to monitor and manage purchase transactions');