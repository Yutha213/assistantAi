-- Run this in your Supabase SQL Editor. 
-- This only adds a search function and will NOT modify your existing table or data.

create or replace function match_knowledge_base (
  query_embedding vector(768), -- Detected dimension: 768 (Jina v2)
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    knowledge_base.id,
    knowledge_base.content,
    knowledge_base.metadata,
    1 - (knowledge_base.embedding <=> query_embedding) as similarity
  from knowledge_base
  where 1 - (knowledge_base.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
end;
$$;
