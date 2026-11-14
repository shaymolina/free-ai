-- Free AI: פרופילים, התקדמות ואירועים

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text,
  full_name text,
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);

create table public.progress (
  user_id uuid not null references auth.users (id) on delete cascade,
  lesson_key text not null,
  completed_at timestamptz not null default now(),
  primary key (user_id, lesson_key)
);

create table public.events (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users (id) on delete set null,
  type text not null check (type in ('view', 'complete', 'click', 'download', 'certificate')),
  target text not null,
  created_at timestamptz not null default now()
);
create index events_type_target_idx on public.events (type, target);
create index events_user_idx on public.events (user_id);

-- פרופיל נוצר אוטומטית בהרשמה
create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, email, full_name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data ->> 'full_name', new.raw_user_meta_data ->> 'name'));
  return new;
end $$;

create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

create function public.is_admin() returns boolean
language sql stable security definer set search_path = '' as $$
  select coalesce((select is_admin from public.profiles where id = (select auth.uid())), false);
$$;

alter table public.profiles enable row level security;
alter table public.progress enable row level security;
alter table public.events enable row level security;

create policy "own profile read" on public.profiles for select to authenticated
  using (id = (select auth.uid()) or (select public.is_admin()));
create policy "own profile name" on public.profiles for update to authenticated
  using (id = (select auth.uid())) with check (id = (select auth.uid()) and is_admin = false);

create policy "own progress read" on public.progress for select to authenticated
  using (user_id = (select auth.uid()) or (select public.is_admin()));
create policy "own progress write" on public.progress for insert to authenticated
  with check (user_id = (select auth.uid()));
create policy "own progress delete" on public.progress for delete to authenticated
  using (user_id = (select auth.uid()));

create policy "own events write" on public.events for insert to authenticated
  with check (user_id = (select auth.uid()));
create policy "admin events read" on public.events for select to authenticated
  using ((select public.is_admin()));
