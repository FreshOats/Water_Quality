-- I want to ultimately figure out a primary key for this table
-- There are duplicates of the station_id, name, ets because there are multiple parameters measured at each
-- Likewise, there are duplicate parameters; however I'd like to determine whether the combination of station_id and parameter will work
-- Since there is a date in the record, it is likely that the date will need to be included, but keeping the number of references minimal is ideal

-- This will give the total number of 
SELECT	COUNT(*) AS total_measurements
FROM	lab_results;
-- This returned 4520815


-- A quick way to see if any single column can provide a primary key
SELECT	COUNT(station_id) id, 
		COUNT(station_name) short_name,  
		COUNT(full_station_name) full_name, 
		COUNT(station_type) station_type, 
		COUNT(sample_code) code, 
		COUNT(parameter) parameter, 
		COUNT(DISTINCT(station_id)) d_id, 
		COUNT(DISTINCT(station_name)) d_short_name,  
		COUNT(DISTINCT(full_station_name)) d_full_name, 
		COUNT(DISTINCT(station_type)) d_station_type, 
		COUNT(DISTINCT(sample_code)) d_code, 
		COUNT(DISTINCT(parameter)) d_parameter
FROM lab_results;
-- Sadly, this is not the case



-- This query will separate the station_id and parameters to see if there are overlapping values. 
SELECT	station_id, parameter
FROM	lab_results
GROUP BY station_id, parameter
ORDER BY parameter DESC;
-- There were only 720,139 rows this time, therefore were are including duplicate values, and we must add another parameter

SELECT	station_id, 
		parameter,
		sample_date
FROM	lab_results
GROUP BY	station_id,  
			parameter,
			sample_date
ORDER BY parameter DESC;
-- 4437329 rows, closer. next going to add the sample_code


-- This includes the sample_date within the grouping
SELECT	station_id, 
		sample_code, 
		parameter,
		sample_date
FROM	lab_results
GROUP BY	station_id, 
			sample_code, 
			parameter,
			sample_date
ORDER BY parameter DESC;
-- This returned 4437329 rows, still fewer than the 4520815
-- Looking at the data, some of the measurements were taken at different depth levels with the same sample date and all other parameters would be the same, so sample depth will be incorporated


SELECT	station_id, 
		sample_depth, 
		parameter,
		sample_date
FROM	lab_results
GROUP BY	station_id, 
			sample_depth, 
			parameter,
			sample_date
ORDER BY parameter DESC;
-- This removed sample code, but added the sample_depth
-- returned 4480726; close but not all

SELECT	station_id, 
		sample_code, 
		parameter,
		sample_date, 
		sample_depth
FROM	lab_results
GROUP BY	station_id, 
			sample_code, 
			parameter,
			sample_date, 
			sample_depth
ORDER BY parameter DESC;
-- 4487917

--Trying something different, going to look for actual duplicate rows in the dataset
SELECT	station_id, 
		station_name, 
		full_station_name, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		sample_depth_units, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_name, 
		full_station_name, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		sample_depth_units, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name
HAVING	COUNT(*) > 1;
-- This returned an empty set, so there are no truly duplicate rows. Now I can systematically remove columns until I can find the full unique key. 
-- Alternatively, since I know that each row is unique, I could opt to give them ID numbers, but it isn't good practice to give arbitrary ID values if unnecessary


SELECT	station_id, 
		station_name, 
		full_station_name, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		sample_depth_units, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_name, 
		full_station_name, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		sample_depth_units, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name
HAVING	COUNT(*) > 1;

-- Station_number, name, and full_name should be redundant, but if they're not... 
SELECT	station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		sample_depth_units, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		sample_depth_units, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name
HAVING	COUNT(*) > 1;
-- Empty set.  

-- Remove the units and reporting limits
SELECT	station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		method_name
HAVING	COUNT(*) > 1;
-- One of those killed it

SELECT	station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name
HAVING	COUNT(*) > 1;
-- Sample depth units were unnecessary

SELECT	station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		station_type, 
		latitude, 
		longitude, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		method_name
HAVING	COUNT(*) > 1;
-- Both Units and Reporting limit are required for uniqueness

-- Try removing station type, latitude and longitude
SELECT	station_id, 
		station_number, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name, 
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		status_, 
		county_name, 
		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name
HAVING	COUNT(*) > 1;
-- empty set; try removing status, county name
-- method_name is required 

SELECT	station_id, 
		station_number, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- empty set; remove result

SELECT	station_id, 
		station_number, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY station_id, 
		station_number, 
		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- removing result broke it; try removing station_id

SELECT	station_number, 
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY station_number, 
		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- empty set; this means that the station name can be a key rather than station id
-- removing sample_code


SELECT	station_number, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY station_number, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- broken 

--removing station_number
SELECT	
		sample_code, 
		sample_date, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY 		sample_code, 
		sample_date, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- Station_number was unnecessary; removing sample_date

SELECT	sample_code, 
		sample_depth,  
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY sample_code, 
		sample_depth, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- empty set

-- remove sample depth
SELECT	sample_code, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY sample_code, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- empty set

-- remove parameter
SELECT	sample_code, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY sample_code, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- broken

-- Last checks... 
SELECT	sample_code, 
		parameter, 
		result, 
		reporting_limit,
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY sample_code, 
		parameter, 
		result, 
		reporting_limit,
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- units only produces 7 duplicate sets, otherwise, all of these columns are necessary to have a primary key


SELECT COUNT(*) 
FROM lab_results
WHERE sample_code IS NULL;
-- there are no null sample codes

SELECT COUNT(*) 
FROM lab_results
WHERE parameter IS NULL;
-- no null parameters

SELECT COUNT(*) 
FROM lab_results
WHERE result IS NULL;
-- This is a problem, since there are null result 

SELECT COUNT(*) 
FROM lab_results
WHERE reporting_limit IS NULL;
-- this also has 17000 nulls

SELECT COUNT(*) 
FROM lab_results
WHERE units IS NULL;
-- no nulls

SELECT COUNT(*) 
FROM lab_results
WHERE method_name IS NULL;
-- no nulls

-- Is it possible to eliminate duplicates without including the result and the reporting limit by adding back station_name and sample_date? 
SELECT COUNT(*) 
FROM lab_results
WHERE sample_date IS NULL OR station_name IS NULL;


SELECT	sample_code, 
		parameter, 
		units,
		method_name,
		COUNT(*)
FROM lab_results
GROUP BY sample_code, 
		parameter, 
		units, 
		method_name
HAVING	COUNT(*) > 1;
-- 15242 rows are duplicate after removing result and reporting limit
-- No change by adding the name and date
-- It seems like the only way to get a truly unique value for this table is to create an ID column, but we can just use this as a dimension table

SELECT	station_number,  
		COUNT(*)
FROM stations
GROUP BY station_number
HAVING COUNT(*) > 1;
-- Station name is not unique in stations, but station ID and station Number are 

SELECT station_name, station_id, station_number
FROM stations;


-- Are there the same number of station ID and station number in the lab_results table? 
SELECT	COUNT(DISTINCT station_id) AS d_id, 
		COUNT(station_id) AS ct_id, 
		COUNT(DISTINCT station_name) as d_name,
		COUNT(station_name) AS ct_name
FROM lab_results;

-- there are the same number of rows, but there are more distinct IDs than there are names
-- Since there are no null values here, we will use the station_id as the foreign key to the stations 



SELECT station_id, 
		parameter, 
		COUNT(*)
FROM period_of_record
GROUP BY station_id, 
		parameter
HAVING COUNT(*) > 1;
-- In period of Record, the station_id and parameter together make a unique identifier


SELECT station_id, 
		parameter,
		sample_code,
		uns_name,
		mth_name,
		COUNT(*)
FROM field_results
GROUP BY station_id, 
		parameter, 
		sample_code,
		uns_name,
		mth_name
HAVING COUNT(*) > 1;
-- In period of Record, the station_id and parameter together make a unique identifier

SELECT COUNT(*) 
FROM field_results
WHERE --station_id IS NULL 
		--parameter IS NULL
		--sample_code IS NULL 
		--uns_name IS NULL 
		mth_name IS NULL 