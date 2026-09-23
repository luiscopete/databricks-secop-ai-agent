CREATE OR REPLACE FUNCTION secop_ai.ai_agents_tools.summary_by_department(
    departamento STRING COMMENT 'Department name to analyze'
)
RETURNS STRING
DETERMINISTIC
COMMENT 'Get statistical summary of contracts for a specific department. Returns aggregated metrics formatted as a message.'
RETURN (
    SELECT CONCAT(
        'Department: ', entidad_departamento, '\n',
        'Total Contracts: ', COUNT(*), '\n',
        'Total Budget: $', FORMAT_NUMBER(SUM(precio_base), 0), ' COP\n',
        'Average Budget: $', FORMAT_NUMBER(AVG(precio_base), 0), ' COP\n',
        'Minimum Budget: $', FORMAT_NUMBER(MIN(precio_base), 0), ' COP\n',
        'Maximum Budget: $', FORMAT_NUMBER(MAX(precio_base), 0), ' COP\n',
        'Unique Entities: ', COUNT(DISTINCT entidad_nombre)
    )
    FROM secop_ai.gold.available_contracts
    WHERE LOWER(entidad_departamento) = LOWER(departamento)
    GROUP BY entidad_departamento
    LIMIT 1
);
