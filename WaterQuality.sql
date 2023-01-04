-- CREATE DATABASE WaterQuality;

DROP TABLE period_of_record;
DROP TABLE field_results;
DROP TABLE lab_results;

CREATE TABLE IF NOT EXISTS period_of_record (
    station_id INT, 
    station_name VARCHAR(250), 
    full_station_name VARCHAR(250), 
    station_number VARCHAR(250), 
    station_type VARCHAR(250),
    latitude FLOAT,
    longitude FLOAT,
    county_name VARCHAR(250),
    parameter VARCHAR(250),
    sample_count INT,
    sample_date_min TIMESTAMP,
    sample_date_max TIMESTAMP
);

CREATE TABLE IF NOT EXISTS field_results (
    station_id INT, 
    station_name VARCHAR,
    station_number VARCHAR,
    full_station_name VARCHAR, 
    station_type VARCHAR,
    latitude FLOAT,
    longitude FLOAT,
    status_ VARCHAR,
    county_name VARCHAR,
    sample_code VARCHAR,
    sample_date TIMESTAMP,
    sample_depth FLOAT,
    sample_depth_units VARCHAR,
    anl_data_type VARCHAR,
    parameter VARCHAR, 
    fdr_result FLOAT,
    fdr_text_result VARCHAR,
    fdr_date_result VARCHAR,
    fdr_reporting_limit FLOAT, 
    uns_name VARCHAR(50),
    mth_name VARCHAR,
    fdr_footnote VARCHAR
);



CREATE TABLE IF NOT EXISTS field_results ( 
    station_id INT,
    station_name VARCHAR,
    station_number VARCHAR,
    full_station_name VARCHAR,
    station_type VARCHAR,
    latitude FLOAT,
    longitude FLOAT,
    status_ VARCHAR,
    county_name VARCHAR,
    sample_code VARCHAR,
    sample_date TIMESTAMP,
    sample_depth FLOAT,
    sample_depth_units VARCHAR,
    anl_data_type VARCHAR,
    parameter VARCHAR,
    fdr_result FLOAT,
    fdr_text_result VARCHAR,
    fdr_date_result VARCHAR,
    fdr_reporting_limit FLOAT,
    uns_name VARCHAR,
    mth_name VARCHAR,
    fdr_footnote VARCHAR
)


CREATE TABLE IF NOT EXISTS lab_results (
    station_id INT, 
    station_name VARCHAR(250), 
    full_station_name VARCHAR(250), 
    station_number VARCHAR(250), 
    station_type VARCHAR(250),
    latitude FLOAT,
    longitude FLOAT,
    status_ VARCHAR(250),
    county_name VARCHAR(250),
    sample_code VARCHAR(250),
    sample_date TIMESTAMP,
    sample_depth VARCHAR(25),
    sample_depth_units VARCHAR(250),
    parameter VARCHAR(250), 
    result FLOAT,
    reporting_limit FLOAT,
    units VARCHAR(250),
    method_name VARCHAR(250)
);
