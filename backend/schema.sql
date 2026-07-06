-- LilyCare PostgreSQL schema starter.
-- You can edit this freely when you decide how strict you want the database to be.

create table if not exists pet_profile (
    id serial primary key,
    name text not null,
    birth_date date,
    description text not null default ''
);

create table if not exists vaccines (
    id serial primary key,
    name text not null,
    description text not null default '',
    note text not null default '',
    recurrence_months integer not null,
    next_due date
);

create table if not exists vaccine_history (
    id serial primary key,
    vaccine_id integer not null references vaccines(id) on delete cascade,
    administered_on date not null
);

create table if not exists vet_links (
    id serial primary key,
    name text not null,
    url text not null,
    notes text not null default ''
);
