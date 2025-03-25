CREATE TABLE IF NOT EXISTS  bronze.ibge00_agregados_municipios_2022 (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS  bronze.ibge01_municipios (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS  bronze.ibge02_pib (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS  bronze.ibge03_populacao_territorio (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS  bronze.ibge04_empregos (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS  bronze.ibge05_ensino_superior (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS  bronze.zapimoveis (
	id SERIAL PRIMARY KEY,
	name_file VARCHAR NOT NULL UNIQUE,
	file_json JSON NOT NULL
);