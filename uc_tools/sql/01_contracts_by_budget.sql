CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.contracts_by_budget(
    min_budget DOUBLE COMMENT 'Minimum budget in COP',
    max_budget DOUBLE COMMENT 'Maximum budget in COP'
)
RETURNS TABLE(
    id_proceso STRING,
    entidad_nombre STRING,
    procedimiento_nombre STRING,
    tipo_contrato STRING,
    precio_base DOUBLE,
    entidad_departamento STRING,
    entidad_ciudad STRING,
    estado_procedimiento STRING
)
COMMENT 'Find contracts within a specific budget range. Useful for filtering by contract size.'
RETURN
    SELECT
        id_proceso,
        entidad_nombre,
        procedimiento_nombre,
        tipo_contrato,
        precio_base,
        entidad_departamento,
        entidad_ciudad,
        estado_procedimiento
    FROM secop_ai.gold.available_contracts
    WHERE precio_base BETWEEN min_budget AND max_budget
    ORDER BY precio_base DESC
    LIMIT 100;
