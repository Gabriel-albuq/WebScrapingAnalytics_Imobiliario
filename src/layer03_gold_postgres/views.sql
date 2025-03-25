CREATE VIEW gold.vi_imoveis_ibge AS
SELECT 
	-- Tabela zapimoveis
    z1.state_name,
    z1.city_name, 
	z1.update_at AS update_at_imoveis,
    COUNT(DISTINCT z1.property_id) AS Qtd_imoveis,
	COUNT(DISTINCT
		CASE
			WHEN z1.type_realese = 'Na planta' THEN z1.property_id
		END) AS Qtd_type_realese_planta,
	COUNT(DISTINCT
		CASE
			WHEN z1.type_realese = 'Em construção' THEN z1.property_id
		END) AS Qtd_type_realese_construcao,
	COUNT(DISTINCT
		CASE
			WHEN z1.type_realese = 'Pronto para morar' THEN z1.property_id
		END) AS Qtd_type_realese_pronto,
	COUNT(DISTINCT
		CASE
			WHEN z1.type_realese NOT IN ('Na planta', 'Em construção', 'Pronto para morar') THEN z1.property_id
		END) AS Qtd_type_realese_outros,
    COUNT(DISTINCT
		CASE 
			WHEN z1.price IS NOT NULL AND price != '' THEN z1.property_id
		END) AS Qtd_imoveis_price,
	ROUND(AVG(
		CASE 
	    	WHEN z1.price IS NOT NULL AND z1.price != '' THEN CAST(z1.price AS NUMERIC)
	    END),2) AS avg_price,
	COUNT(DISTINCT
		CASE 
	    	WHEN z1.area IS NOT NULL AND z1.area != '' THEN CAST(z1.area AS NUMERIC)
	    END) AS qtd_area,
	ROUND(AVG(
		CASE 
	    	WHEN z1.area IS NOT NULL AND z1.area != '' THEN CAST(z1.area AS NUMERIC)
	    END),2) AS avg_area,
	ROUND(AVG(z1.area_price_ratio),2) AS avg_area_price_ratio,
	-- Tabela ibge02_pib
	COALESCE(CAST(i2.serie AS VARCHAR), 'N/A') AS pib_year,
	i2.unidade AS pib_unidade,
	MAX(i2.valor_serie) AS pib_value,
	-- Tabela ibge03_populacao_territorio (93-Populacao residente)
	COALESCE(CAST(i3_93.serie AS VARCHAR), 'N/A') AS populacao_year,
    i3_93.unidade AS populacao_unidade,
    MAX(i3_93.valor_serie) AS populacao_value,
	-- Tabela ibge03_populacao_territorio (6318-Área Territorial)
	COALESCE(CAST(i3_6318.serie AS VARCHAR), 'N/A') AS area_territorial_year,
    i3_6318.unidade AS area_territorial_unidade,
    MAX(i3_6318.valor_serie) AS area_territorial_value,
	-- Tabela ibge04_empregos (706-Número de Unidades Locais)
	COALESCE(CAST(i4_706.serie AS VARCHAR), 'N/A') AS unidades_locais_year,
    i4_706.unidade AS unidades_locais_unidade,
    MAX(i4_706.valor_serie) AS unidades_locais_value,
	-- Tabela ibge04_empregos (707-Pessoal ocupado total)
	COALESCE(CAST(i4_707.serie AS VARCHAR), 'N/A') AS pessoal_ocupado_year,
    i4_707.unidade AS pessoal_ocupado_unidade,
    MAX(i4_707.valor_serie) AS pessoal_ocupado_value,
	-- Tabela ibge04_empregos (10143-Salário medio mensal em reais)
	COALESCE(CAST(i4_10143.serie AS VARCHAR), 'N/A') AS salario_medio_year,
    i4_10143.unidade AS salario_medio_unidade,
    MAX(i4_10143.valor_serie) AS salario_medio_value,
	-- Tabela ibge05_ensino_superior
	COALESCE(CAST(i5.serie AS VARCHAR), 'N/A') AS ensino_superior_year,
    i5.unidade AS ensino_superior_unidade,
    MAX(i5.valor_serie) AS ensino_superior_value
FROM 
    gold.zapimoveis z1
LEFT JOIN 
    silver.ibge02_pib i2
ON 
    LOWER(z1.city_state_name) = LOWER(i2.nome_localidade)
	AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge02_pib
        WHERE serie <= z1.year_update_at
    )
LEFT JOIN 
	(SELECT * 
	FROM silver.ibge03_populacao_territorio
	WHERE id_pesquisa = 93) i3_93
ON 
    LOWER(z1.city_state_name) = LOWER(i3_93.nome_localidade)
    AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge03_populacao_territorio
        WHERE 
			serie <= z1.year_update_at
			AND id_pesquisa = 93
    )
LEFT JOIN 
	(SELECT * 
	FROM silver.ibge03_populacao_territorio
	WHERE id_pesquisa = 6318) i3_6318
ON 
    LOWER(z1.city_state_name) = LOWER(i3_6318.nome_localidade)
    AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge03_populacao_territorio
        WHERE 
			serie <= z1.year_update_at
			AND id_pesquisa = 6318
    )
LEFT JOIN 
	(SELECT * 
	FROM silver.ibge04_empregos
	WHERE id_pesquisa = 706) i4_706
ON 
    LOWER(z1.city_state_name) = LOWER(i4_706.nome_localidade)
    AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge04_empregos
        WHERE 
			serie <= z1.year_update_at
			AND id_pesquisa = 706
    )
LEFT JOIN 
	(SELECT * 
	FROM silver.ibge04_empregos
	WHERE id_pesquisa = 707) i4_707
ON 
    LOWER(z1.city_state_name) = LOWER(i4_707.nome_localidade)
    AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge04_empregos
        WHERE 
			serie <= z1.year_update_at
			AND id_pesquisa = 707
    )
LEFT JOIN 
	(SELECT * 
	FROM silver.ibge04_empregos
	WHERE id_pesquisa = 10143) i4_10143
ON 
    LOWER(z1.city_state_name) = LOWER(i4_10143.nome_localidade)
    AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge04_empregos
        WHERE 
			serie <= z1.year_update_at
			AND id_pesquisa = 10143
    )
LEFT JOIN 
	silver.ibge05_ensino_superior i5
ON 
    LOWER(z1.city_state_name) = LOWER(i5.nome_localidade)
    AND CAST(z1.year_update_at AS INTEGER) >= (
        SELECT CAST(MAX(serie) AS INTEGER)  
        FROM silver.ibge05_ensino_superior
        WHERE 
			serie <= z1.year_update_at
    )
GROUP BY
    z1.state_name,
    z1.city_name, 
    z1.update_at,
	i2.serie,
	i2.unidade,
	i3_93.serie,
    i3_93.unidade,
	i3_6318.serie,
    i3_6318.unidade,
	i4_706.serie,
    i4_706.unidade,
	i4_707.serie,
    i4_707.unidade,
	i4_10143.serie,
    i4_10143.unidade,
	i5.serie,
	i5.unidade


DROP VIEW gold.vi_imoveis_ibge