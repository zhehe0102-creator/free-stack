-- Supabase 免费档：Postgres 500MB/项目，最多 2 个活跃项目
-- 闲置 1 周自动暂停，需手动恢复；超 500MB 变只读
-- 在 Supabase Dashboard > SQL Editor 里执行

create table if not exists jobs (
  id uuid primary key default gen_random_uuid(),
  kind text not null,               -- 'train' | 'inference' | 'sync'
  status text not null default 'queued', -- queued | running | done | failed
  payload jsonb default '{}'::jsonb,
  result jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists results (
  id uuid primary key default gen_random_uuid(),
  job_id uuid references jobs(id) on delete cascade,
  title text,
  file_url text,                    -- R2 公开 / 签名 URL
  meta jsonb default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_jobs_status_created on jobs (status, created_at desc);
create index if not exists idx_results_job on results (job_id);
