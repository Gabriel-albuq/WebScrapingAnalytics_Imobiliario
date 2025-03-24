SELECT 
    t1.state_name, 
    t1.city_name, 
    t2.nome_localidade
FROM 
    gold.zapimoveis t1
LEFT JOIN 
    silver.ibge05_ensino_superior t2 
ON 
    CONCAT(t1.city_name, ' - ', t1.state_name) = t2.nome_localidade;
