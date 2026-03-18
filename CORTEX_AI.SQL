create or replace semantic view STRT_DB_SI.LORELAI.LORELAI_SEMANTIC_VIEW
	tables (
		STRT_DB_SI.LORELAI.STATIONS_CLEANED primary key (STATIONNAME) comment='The table contains records of stations, including their identifying names, brand affiliations, and physical locations.',
		STRT_DB_SI.LORELAI.STOPS_CLEANED primary key (STOPDT) comment='The table contains records of fuel stops, capturing details about each refueling event. Each record includes information about the station, date, fuel quantity, pricing, payment, and mileage associated with a given trip.',
		STRT_DB_SI.LORELAI.STOPS_WITH_DIFFS primary key (STOPDT) comment='The table contains records of fuel stops, capturing details about each refueling event. Each record includes information about the station, date, fuel quantity and cost, mileage, and trip association, along with calculated differences in mileage and time between stops.'
	)
	relationships (
		STOPS_CLEANED_TO_STATIONS_CLEANED as STOPS_CLEANED(STATIONNAME) references STATIONS_CLEANED(STATIONNAME)
	)
	facts (
		STOPS_CLEANED.CREDIT as CREDIT comment='The amount of credit associated with a stop.',
		STOPS_CLEANED.GAL as GAL comment='The number of gallons associated with a stop.',
		STOPS_CLEANED.MILES as MILES comment='The distance traveled in miles.',
		STOPS_CLEANED.PRICE as PRICE comment='The price associated with a stop.',
		STOPS_CLEANED.TRIP as TRIP comment='The distance or duration of a trip.',
		STOPS_WITH_DIFFS.CREDIT as CREDIT comment='A column holding data of type FLOAT.',
		STOPS_WITH_DIFFS.DAYS_BETWEEN as DAYS_BETWEEN comment='The number of days between two stops.',
		STOPS_WITH_DIFFS.GAL as GAL comment='The volume of fuel measured in gallons.',
		STOPS_WITH_DIFFS.MILES as MILES comment='The distance measured in miles.',
		STOPS_WITH_DIFFS.MILES_DIFF as MILES_DIFF comment='The difference in miles between two recorded values for a stop.',
		STOPS_WITH_DIFFS.PRICE as PRICE comment='The price associated with a stop, represented as a floating-point number.',
		STOPS_WITH_DIFFS.ROWID as ROWID comment='A unique numeric identifier assigned to each row in the table.',
		STOPS_WITH_DIFFS.TRIP as TRIP comment='A numeric identifier for a trip.'
	)
	dimensions (
		STATIONS_CLEANED.ADDRESS as ADDRESS comment='The street address associated with the station location.',
		STATIONS_CLEANED.BRAND as BRAND comment='The brand name of the fuel station.',
		STATIONS_CLEANED.ROWID as ROWID comment='A unique sequential identifier assigned to each row.',
		STATIONS_CLEANED.STATIONNAME as STATIONNAME comment='The name of the fuel station.',
		STOPS_CLEANED.ROWID as ROWID comment='A unique numeric identifier assigned to each row.',
		STOPS_CLEANED.STATIONNAME as STATIONNAME comment='The name of the fuel station associated with a stop.',
		STOPS_CLEANED.STOPDT as STOPDT comment='The date and time when a stop occurred.',
		STOPS_WITH_DIFFS.STATIONNAME as STATIONNAME comment='The name of the station associated with a stop.',
		STOPS_WITH_DIFFS.STOPDT as STOPDT comment='The date and time when a stop occurred.'
	)
	metrics (
		STOPS_CLEANED.AGG_MPG as SUM(TRIP)/SUM(GAL) comment='Calculated Miles per Gallon',
		STOPS_CLEANED.TOTAL_COST as SUM(CREDIT) comment='Total amount paid for fuel',
		STOPS_CLEANED.TOTAL_TRIP_MI as SUM(TRIP) comment='Cumulative Trip Mileage'
	)
	with extension (CA='{"tables":[{"name":"STATIONS_CLEANED","dimensions":[{"name":"ADDRESS","sample_values":["2 Waukegan Rd, Deerfield, IL 60015","Unknown","3700 W Addison St, Chicago, IL 60618"]},{"name":"BRAND","sample_values":["Shell","BP","Mobil"]},{"name":"ROWID","sample_values":["6","0","1"]},{"name":"STATIONNAME","sample_values":["Deerfield Shell","BP 8937807","BP 8886525"]}]},{"name":"STOPS_CLEANED","dimensions":[{"name":"ROWID","sample_values":["0","1","75"]},{"name":"STATIONNAME","sample_values":["Deerfield Shell","BP 8937807","BP 8886525"]}],"facts":[{"name":"CREDIT","sample_values":["19.09","23.68","47.28"]},{"name":"GAL","sample_values":["5.816","9.252","6.239"]},{"name":"MILES","sample_values":["12378","8921","12574"]},{"name":"PRICE","sample_values":["2.799","3.279","2.849"]},{"name":"TRIP","sample_values":["212.8","210.9","166"]}],"metrics":[{"name":"AGG_MPG"},{"name":"TOTAL_COST"},{"name":"TOTAL_TRIP_MI"}],"time_dimensions":[{"name":"STOPDT","sample_values":["2019-07-17T07:46:00.000+0000","2020-03-06T07:41:00.000+0000","2019-09-19T08:14:00.000+0000"]}]},{"name":"STOPS_WITH_DIFFS","dimensions":[{"name":"STATIONNAME","sample_values":["3700 W Addison Shell","BP 5210 Northwest Hwy","BP 8937807"]}],"facts":[{"name":"CREDIT","sample_values":["24.12","23.48","16.5"]},{"name":"DAYS_BETWEEN","sample_values":["37","63"]},{"name":"GAL","sample_values":["9.252","5.806","7.04"]},{"name":"MILES","sample_values":["14255","4220","14479"]},{"name":"MILES_DIFF","sample_values":["228","46"]},{"name":"PRICE","sample_values":["2.489","3.279","3.059"]},{"name":"ROWID","sample_values":["1","68","18"]},{"name":"TRIP","sample_values":["151.5","175.7","210.9"]}],"time_dimensions":[{"name":"STOPDT","sample_values":["2019-07-17T07:46:00.000+0000","2019-09-19T08:14:00.000+0000","2022-12-01T08:19:00.000+0000"]}]}],"relationships":[{"name":"STOPS_CLEANED_TO_STATIONS_CLEANED","join_type":"inner"}]}');

create or replace cortex search service STRT_DB_SI.LORELAI.LORELAI_SEARCH_SERVICE
	ON STATIONNAME
	attributes STATIONNAME,ROWID,STOPDT,CREDIT,GAL,PRICE,MILES,TRIP
	warehouse='STRT_WH_SI'
	target_lag='1 hour'
	refresh_mode=INCREMENTAL
	as (
	SELECT
		STATIONNAME,
		ROWID,
		STOPDT,
		CREDIT,
		GAL,
		PRICE,
		MILES,
		TRIP
	FROM STRT_DB_SI.LORELAI.STOPS_CLEANED
);
