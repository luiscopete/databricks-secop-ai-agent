CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.high_value_contracts(
    threshold DOUBLE COMMENT 'Minimum budget threshold in COP (default: 100,000,000)'
)
RETURNS TABLE(
    id_proceso STRING,
    entidad_nombre STRING,
    procedimiento_nombre STRING,
    tipo_contrato STRING,
    precio_base DOUBLE,
    entidad_departamento STRING,
    modalidad_contratacion STRING,
    estado_procedimiento STRING
)
COMMENT 'Find high-value contracts above a specified budget threshold. Useful for identifying major opportunities.'
RETURN
    SELECT
        id_proceso,
        entidad_nombre,
        procedimiento_nombre,
        tipo_contrato,
        precio_base,
        entidad_departamento,
        modalidad_contratacion,
        estado_procedimiento
    FROM secop_ai.gold.available_contracts
    WHERE precio_base >= threshold
    ORDER BY precio_base DESC
    LIMIT 100;
