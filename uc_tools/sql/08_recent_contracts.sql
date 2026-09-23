CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.recent_contracts(
    days_back INT COMMENT 'Number of days to look back (default: 7)'
)
RETURNS TABLE(
    id_proceso STRING,
    entidad_nombre STRING,
    procedimiento_nombre STRING,
    tipo_contrato STRING,
    precio_base DOUBLE,
    entidad_departamento STRING,
    fecha_ultima_publicacion TIMESTAMP,
    days_since_publication INT
)
COMMENT 'Get contracts published within the last N days. Returns most recent contracts first.'
RETURN
    SELECT
        id_proceso,
        entidad_nombre,
        procedimiento_nombre,
        tipo_contrato,
        precio_base,
        entidad_departamento,
        fecha_ultima_publicacion,
        DATEDIFF(
            CURRENT_DATE(),
            DATE(fecha_ultima_publicacion)
        ) AS days_since_publication
    FROM secop_ai.gold.available_contracts
    WHERE fecha_ultima_publicacion >= DATE_SUB(CURRENT_DATE(), days_back)
    ORDER BY fecha_ultima_publicacion DESC
    LIMIT 100;
