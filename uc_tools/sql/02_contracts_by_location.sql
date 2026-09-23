CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.contracts_by_location(
    departamento STRING COMMENT 'Department name (e.g., "Bogotá D.C.", "Antioquia")'
)
RETURNS TABLE(
    id_proceso STRING,
    entidad_nombre STRING,
    entidad_ciudad STRING,
    procedimiento_nombre STRING,
    tipo_contrato STRING,
    precio_base DOUBLE,
    estado_procedimiento STRING,
    fecha_ultima_publicacion TIMESTAMP
)
COMMENT 'Get all active contracts for a specific department. Returns contracts ordered by publication date.'
RETURN
    SELECT
        id_proceso,
        entidad_nombre,
        entidad_ciudad,
        procedimiento_nombre,
        tipo_contrato,
        precio_base,
        estado_procedimiento,
        fecha_ultima_publicacion
    FROM secop_ai.gold.available_contracts
    WHERE LOWER(entidad_departamento) = LOWER(departamento)
    ORDER BY fecha_ultima_publicacion DESC
    LIMIT 100;
