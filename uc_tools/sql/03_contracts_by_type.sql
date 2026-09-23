CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.contracts_by_type(
    contract_type STRING COMMENT 'Contract type (e.g., "Prestación de servicios", "Compraventa")'
)
RETURNS TABLE(
    id_proceso STRING,
    entidad_nombre STRING,
    procedimiento_nombre STRING,
    tipo_contrato STRING,
    subtipo_contrato STRING,
    precio_base DOUBLE,
    duracion INT,
    duracion_unidad STRING,
    entidad_departamento STRING
)
COMMENT 'Filter contracts by type (e.g., services, purchase, construction). Returns matching active contracts.'
RETURN
    SELECT
        id_proceso,
        entidad_nombre,
        procedimiento_nombre,
        tipo_contrato,
        subtipo_contrato,
        precio_base,
        duracion,
        duracion_unidad,
        entidad_departamento
    FROM secop_ai.gold.available_contracts
    WHERE LOWER(tipo_contrato) LIKE CONCAT('%', LOWER(contract_type), '%')
    ORDER BY precio_base DESC
    LIMIT 100;
