use role accountadmin;

create or replace role strtest_admin;
grant create warehouse on account to role strtest_admin;
grant create database on account to role strtest_admin;
grant create integration on account to role strtest_admin;

set current_user = (select current_user());   
grant role strtest_admin to user identifier($current_user);
alter user set default_role = strtest_admin;
alter user set default_warehouse = strt_wh_si;

use role strtest_admin;
create or replace database strt_db_si;
create or replace schema lorelai;
create or replace warehouse strt_wh_si with warehouse_size='large';

use role snowflake_intelligence_admin;
create database if not exists snowflake_intelligence;
create schema if not exists snowflake_intelligence.agents;

grant create agent on schema snowflake_intelligence.agents to role strtest_admin;

use role strtest_admin;
use database strt_db_si;
use schema lorelai;
use warehouse strt_wh_si;

-- create git api integration and repository
create or replace api integration markspotsthex_liesel_si_git_api_integration
  api_provider = git_https_api
  api_allowed_prefixes = ('https://github.com/markspotsthex')
  enabled = true;

create or replace git repository markspotsthex_liesel_si_repo
  api_integration = markspotsthex_liesel_si_git_api_integration
  origin = 'https://github.com/markspotsthex/Liesel';


create or replace file format swt_jsonformat  
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE
  STRIP_NULL_VALUES = TRUE;
  
-- create stage and load data from github bucket
create or replace stage swt_liesel_data_stage
    encryption = (type = 'snowflake_sse')
    directory = (enable = true)
;

-- copy JSON data from git repo to stage
copy files into @swt_liesel_data_stage
  from @markspotsthex_liesel_si_repo/branches/main/
  files = ('Liesel_Fuel_History.json');

-- List files to confirm access
LIST @swt_liesel_data_stage;

-- Query JSON directly from the stage
SELECT $1:stations
FROM @swt_liesel_data_stage/Liesel_Fuel_History.json (FILE_FORMAT => swt_jsonformat);

SELECT $1:stops
FROM @swt_liesel_data_stage/Liesel_Fuel_History.json (FILE_FORMAT => swt_jsonformat);

create or replace table lorelai.stations_raw as 
SELECT $1:stations as stations_raw
FROM @swt_liesel_data_stage/Liesel_Fuel_History.json (FILE_FORMAT => swt_jsonformat);

desc table lorelai.stations_raw;

create or replace table lorelai.stations_cleaned as
select 
  index as rowID
, value:stationName::VARCHAR as stationName
, value:attributes:brand::VARCHAR as brand
, value:attributes:location:address::VARCHAR as address
from lorelai.stations_raw, LATERAL FLATTEN(input => stations_raw);

create or replace table lorelai.stops_raw as 
SELECT $1:stops as stops_raw
FROM @swt_liesel_data_stage/Liesel_Fuel_History.json (FILE_FORMAT => swt_jsonformat);

desc table lorelai.stops_raw;

create or replace table lorelai.stops_cleaned as
select 
  index as rowID
, value:stationName::VARCHAR as stationName
, value:datetime::datetime as stopDt
, value:credit::FLOAT as credit
, value:gal::float as gal
, value:price::FLOAT as price
, value:miles::INT as miles
, value:trip::FLOAT as trip
from lorelai.stops_raw, LATERAL FLATTEN(input => stops_raw);

create or replace view lorelai.stops_with_diffs as
select *
, s.miles - LAG(s.miles) OVER (ORDER BY s.stopdt asc) AS miles_diff
, sum(s.trip) OVER (ORDER BY s.stopdt asc) AS cumulative_trip_miles
, datediff('day', LAG(s.stopdt) OVER (ORDER BY s.stopdt asc), s.stopdt) as days_between
from lorelai.stops_cleaned as s
order by s.stopdt
;
