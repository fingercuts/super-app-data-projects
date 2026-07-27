-- Macro to resolve data path for parquet files
-- Usage: {{ resolve_data_path('users.parquet') }}
{% macro resolve_data_path(filename) %}
    {{ var('data_path', '../data/production') }}/{{ filename }}
{% endmacro %}
