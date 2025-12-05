# Practical Exam: Weather Station Data Processor API

## Objective

Build a FastAPI application that downloads a data file from a public S3 bucket, parses its contents, stores the structured data in a local SQLite database, and exposes endpoints to query that data.

**Time Limit:** 1 hour

---

## Scenario

You have been tasked with creating a service to analyze weather station data. This data is stored in a public S3 bucket managed by NOAA (National Oceanic and Atmospheric Administration).

---

## Public S3 File Details

- **Bucket Name:** `noaa-ghcn-pds`
- **File Key:** `ghcnd-stations.txt`
- **Region:** `us-east-1`
- **HTTP URL:** `https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-stations.txt`

**Note:** This file uses **space-separated** (fixed-width) format instead of tab-separated. The file contains weather station data with the following structure per line:
- Station ID (11 chars)
- Latitude (9 chars) 
- Longitude (10 chars)
- Elevation (7 chars)
- State (2 chars)
- Station Name (30 chars)
- GSN Flag (3 chars)
- HCN/CRN Flag (3 chars)
- WMO ID (5 chars)

---

## Data Format

Each line is a **fixed-width** (space-separated) record. Parse the following fields from each line:

### Example Lines:

```
ACW00011604  17.1167  -61.7833   10.1    ST JOHNS COOLIDGE FLD                       
ACW00011647  17.1333  -61.7833   19.2    ST JOHNS                                    
AE000041196  25.3330   55.5170   34.0    SHARJAH INTER. AIRP            GSN     41196
```

### Field Mapping (Fixed-Width Parsing):

| Position | Field Name        | Data Type          | Width | Notes                                  |
| :-------- | :---------------- | :----------------- | :---- | :------------------------------------- |
| 0-10     | `station_id`      | `str`              | 11    | Station identifier                     |
| 12-20    | `latitude`        | `float`            | 9     | Latitude in degrees                    |
| 21-30    | `longitude`       | `float`            | 10    | Longitude in degrees                   |
| 31-37    | `elevation`       | `float`            | 7     | Elevation in meters                    |
| 38-40    | `state`           | `str`              | 2     | State code (may be empty)              |
| 41-70    | `station_name`    | `str`              | 30    | Station name (trim whitespace)         |

**Note:** 
- Use string slicing or regex to parse fixed-width format
- Handle empty/missing fields appropriately
- Trim whitespace from string fields

---

## Your Mission (in 1 Hour)

### Step 1: Data Models (Pydantic & SQLAlchemy)

1. **Pydantic Schema:** Create a Pydantic `BaseModel` named `WeatherStation` to represent a single station record. It should include the fields:
   - `station_id` (str)
   - `latitude` (float)
   - `longitude` (float)
   - `elevation` (float)
   - `station_name` (str)

2. **SQLAlchemy Model:** Define a SQLAlchemy ORM model for a `stations` table that corresponds to your Pydantic model. Use **SQLite** for the database.

### Step 2: Business Logic (Boto3, Data Handling)

1. **Fetch from S3:** Write a function using **Boto3** to download the station data file from the public S3 bucket. Handle potential errors gracefully (e.g., network issues, file not found).

2. **Parse the Data:** Write a function that reads the file line-by-line. For each line:
   - Parse the fixed-width format using string slicing or regex
   - Handle potential errors (like lines that are too short or malformed) gracefully
   - Convert the relevant fields to their correct data types (float for numeric fields)
   - Trim whitespace from string fields

3. **Store in Database:** Combine these functions to parse the station records and save each valid record into the SQLite database using a SQLAlchemy session.

### Step 3: API Endpoints (FastAPI)

1. **Ingestion Endpoint (`POST /ingest-stations`):**
   - Triggers the process of downloading, parsing, and storing the station data
   - Returns a summary, e.g., `{"message": "Ingestion complete", "records_processed": 500, "records_saved": 498}`

2. **Query Endpoint (`GET /stations/`):**
   - Retrieves stations from the database
   - Accept an optional query parameter to filter by `station_name` (partial match)
   - The endpoint should return a list of `WeatherStation` objects

---

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the API documentation at: `http://localhost:8000/docs`

---

## Evaluation Criteria

- **Functionality:** Does it work? Can you ingest station data and query it?
- **Correctness:** Are models, parsing, and database operations correct?
- **Code Quality:** Is the code well-structured and maintainable?
- **Problem Solving:** How do you approach debugging and error handling?

---

## Bonus Points (If time permits)

- Adding error handling (e.g., what if the S3 file doesn't exist, or a station record is malformed?)
- Making the DB session a FastAPI dependency
- Using `async/await` for I/O-bound operations

---

## Notes

- The S3 bucket is public, so you don't need AWS credentials
- Use SQLite for simplicity (no external database setup required)
- Focus on getting a working solution first, then optimize if time permits
- The file is approximately 11MB, so consider processing in batches or limiting rows for initial testing
- Fixed-width parsing: Use string slicing (e.g., `line[0:11]`) or regex to extract fields

