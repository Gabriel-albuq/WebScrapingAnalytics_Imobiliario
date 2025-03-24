DROP TABLE 
silver.ibge00_agregados_municipios_2022, 
silver.ibge01_municipios, 
silver.ibge02_pib, 
silver.ibge03_populacao_territorio, 
silver.ibge04_empregos, 
silver.ibge05_ensino_superior;

-- Criando a tabela ibge00_agregados_municipios_2022 no schema silver
CREATE TABLE silver.ibge00_agregados_municipios_2022 (
    categoria_id VARCHAR(10),
    categoria_nome TEXT,
    agregado_id INTEGER PRIMARY KEY,
    agregado_nome TEXT
);

-- Criando a tabela ibge01_municipios no schema silver
CREATE TABLE silver.ibge01_municipios (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    microrregiao_id VARCHAR(50),
    microrregiao_nome VARCHAR(50),
    mesorregiao_id INTEGER,
    mesorregiao_nome VARCHAR(50),
    uf_id INTEGER,
    uf_sigla VARCHAR(2),
    uf_nome VARCHAR(50),
    regiao_id INTEGER,
    regiao_sigla VARCHAR(2),
    regiao_nome VARCHAR(50)
);

-- Criando a tabela ibge02_pib no schema silver
CREATE TABLE silver.ibge02_pib (
    id_pesquisa INTEGER,
    nome_pesquisa VARCHAR(100) NOT NULL,
    unidade VARCHAR(50),
    id_nivel VARCHAR(50),
    nome_nivel VARCHAR(50),
    id_localidade INTEGER,
    nome_localidade VARCHAR(100),
    serie INTEGER,
    valor_serie FLOAT,
    PRIMARY KEY (id_pesquisa, id_localidade, serie),
    FOREIGN KEY (id_localidade) REFERENCES silver.ibge01_municipios(id) ON DELETE CASCADE
);

-- Criando a tabela ibge03_populacao_territorio no schema silver
CREATE TABLE silver.ibge03_populacao_territorio (
    id_pesquisa INTEGER,
    nome_pesquisa VARCHAR(100) NOT NULL,
    unidade VARCHAR(50),
    id_nivel VARCHAR(50),
    nome_nivel VARCHAR(50),
    id_localidade INTEGER,
    nome_localidade VARCHAR(100),
    serie INTEGER,
    valor_serie FLOAT,
    PRIMARY KEY (id_pesquisa, id_localidade, serie),
    FOREIGN KEY (id_localidade) REFERENCES silver.ibge01_municipios(id) ON DELETE CASCADE
);

-- Criando a tabela ibge04_empregos no schema silver
CREATE TABLE silver.ibge04_empregos (
    id_pesquisa INTEGER,
    nome_pesquisa VARCHAR(100) NOT NULL,
    unidade VARCHAR(50),
    id_nivel VARCHAR(50),
    nome_nivel VARCHAR(50),
    id_localidade INTEGER,
    nome_localidade VARCHAR(100),
    serie INTEGER,
    valor_serie FLOAT,
    PRIMARY KEY (id_pesquisa, id_localidade, serie),
    FOREIGN KEY (id_localidade) REFERENCES silver.ibge01_municipios(id) ON DELETE CASCADE
);

-- Criando a tabela ibge05_ensino_superior no schema silver
CREATE TABLE silver.ibge05_ensino_superior (
    id_pesquisa INTEGER,
    nome_pesquisa VARCHAR(100) NOT NULL,
    unidade VARCHAR(50),
    id_nivel VARCHAR(50),
    nome_nivel VARCHAR(50),
    id_localidade INTEGER,
    nome_localidade VARCHAR(100),
    serie INTEGER,
    valor_serie FLOAT,
    PRIMARY KEY (id_pesquisa, id_localidade, serie),
    FOREIGN KEY (id_localidade) REFERENCES silver.ibge01_municipios(id) ON DELETE CASCADE
);