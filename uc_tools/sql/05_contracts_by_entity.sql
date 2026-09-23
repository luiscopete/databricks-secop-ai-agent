CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.contracts_by_entity(
    nit STRING COMMENT 'Entity NIT number'
)
RETURNS TABLE(
    id_proceso STRING,
    entidad_nombre STRING,
    entidad_nit STRING,
    procedimiento_nombre STRING,
    tipo_contrato STRING,
    precio_base DOUBLE,
    estado_procedimiento STRING,
    fecha_publicacion TIMESTAMP,
    fecha_ultima_publicacion TIMESTAMP
)
COMMENT 'Get all contracts published by a specific entity (identified by NIT).'
RETURN
    SELECT
        id_proceso,
        entidad_nombre,
        entidad_nit,
        procedimiento_nombre,
        tipo_contrato,
        precio_base,
        estado_procedimiento,
        fecha_publicacion,
        fecha_ultima_publicacion
    FROM secop_ai.gold.available_contracts
    WHERE entidad_nit = nit
    ORDER BY fecha_ultima_publicacion DESC
    LIMIT 100;
