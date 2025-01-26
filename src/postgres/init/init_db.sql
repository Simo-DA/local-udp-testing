DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dagster') THEN
      CREATE DATABASE dagster;
   END IF;
END
$$;