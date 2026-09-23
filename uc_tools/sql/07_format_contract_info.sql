CREATE OR REPLACE FUNCTION {{catalog}}.{{tools_schema}}.format_contract_info(
    proceso_id STRING COMMENT 'Contract process ID to format'
)
RETURNS STRING
COMMENT 'Format contract information into a human-readable string for agent responses.'
RETURN (
    SELECT CONCAT(
        'Contract ID: ', id_proceso, '\n',
        'Entity: ', entidad_nombre, ' (', entidad_nit, ')\n',
        'Location: ', entidad_ciudad, ', ', entidad_departamento, '\n',
        'Title: ', procedimiento_nombre, '\n',
        'Type: ', tipo_contrato, ' - ', COALESCE(subtipo_contrato, 'N/A'), '\n',
        'Budget: $', FORMAT_NUMBER(precio_base, 0), ' COP\n',
        'Duration: ', COALESCE(CAST(duracion AS STRING), 'N/A'), ' ', COALESCE(duracion_unidad, ''), '\n',
        'Status: ', estado_procedimiento, ' (', fase, ')\n',
        'Published: ', DATE_FORMAT(fecha_publicacion, 'yyyy-MM-dd')
    )
    FROM {{catalog}}.{{gold_schema}}.available_contracts
    WHERE id_proceso = proceso_id
    LIMIT 1
);
