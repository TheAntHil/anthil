# anthil
dll:
-- public.runs определение

-- Drop table

-- DROP TABLE public.runs;

CREATE TABLE public.runs (
  run_id uuid NOT NULL,
  job_id uuid NOT NULL,
  status varchar NOT NULL,
  created_at timestamp NOT NULL,
  updated_at timestamp NOT NULL,
  start_time timestamp NOT NULL,
  CONSTRAINT runs_pkey PRIMARY KEY (run_id)
);