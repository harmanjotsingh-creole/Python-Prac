# Practical Exam: Ad Impression Log Processor API

## Objective

Build a FastAPI application that downloads a log file from a public S3 bucket, parses its contents, stores the structured data in a local SQLite database, and exposes endpoints to query that data.

**Time Limit:** 1 hour

---

## Scenario

You have been tasked with creating a service to analyze ad impression logs. These logs are stored in a public S3 bucket managed by AWS.

---

## Public S3 File Details

- **Bucket Name:** `elasticmapreduce`
- **File Key:** `samples/hive-ads/tables/impressions/dt=2009-04-13-08-05/ec2-0-53-91-4.amazon.com-2009-04-13-08-05.log`
- **Region:** `us-east-1`

---

## Log Format

Each line is a **tab-separated** record. The columns are separated by tabs (`\t`).

### Example Lines:

```
2009-04-13 08:05:02	45	259	259	0.01	NULL	NULL	cnet.com	search.com	NULL	NULL
2009-04-13 08:05:02	45	256	256	0.01	NULL	NULL	cnet.com	search.com	NULL	NULL
2009-04-13 08:05:02	45	257	257	0.01	NULL	NULL	cnet.com	search.com	NULL	NULL
```

### Column Mapping:

| Column Index | Field Name        | Data Type          | Notes                                  |
| :----------- | :---------------- | :----------------- | :------------------------------------- |
| 0            | `impression_time` | `datetime`         | e.g., `2009-04-13 08:05:02`            |
| 1            | `ad_id`           | `int`              |                                        |
| 2            | `creative_id`     | `int`              |                                        |
| 4            | `bid_price`       | `float` or `Decimal` | e.g., `0.01`                           |
| 7            | `ad_domain`       | `str`              | e.g., `cnet.com`                       |
| 8            | `search_query`    | `str`              | e.g., `search.com` or `NULL` if empty |

**Note:** Column indices 3, 5, 6, 9, 10 are not required for this task. Handle `NULL` strings appropriately.

---

## Your Mission (in 1 Hour)

### Step 1: Data Models (Pydantic & SQLAlchemy)

1. **Pydantic Schema:** Create a Pydantic `BaseModel` named `AdImpression` to represent a single log entry. It should include the fields:
   - `impression_time` (datetime)
   - `ad_id` (int)
   - `creative_id` (int)
   - `bid_price` (float)
   - `ad_domain` (str)

2. **SQLAlchemy Model:** Define a SQLAlchemy ORM model for an `impressions` table that corresponds to your Pydantic model. Use **SQLite** for the database.

### Step 2: Business Logic (Boto3, Data Handling)

1. **Fetch from S3:** Write a function using **Boto3** to download the specified log file from the public S3 bucket.

2. **Parse the Logs:** Write a function that reads the file line-by-line. For each line:
   - Split it by tabs
   - Handle potential errors (like lines with incorrect column counts) gracefully
   - Convert the relevant columns to their correct data types
   - Handle the `NULL` strings for non-required fields

3. **Store in Database:** Combine these functions to parse the log entries and save each valid record into the SQLite database using a SQLAlchemy session.

### Step 3: API Endpoints (FastAPI)

1. **Ingestion Endpoint (`POST /ingest-logs`):**
   - Triggers the process of downloading, parsing, and storing the logs
   - Returns a summary, e.g., `{"message": "Ingestion complete", "records_processed": 500, "records_saved": 498}`

2. **Query Endpoint (`GET /impressions/`):**
   - Retrieves logs from the database
   - Accept an optional query parameter to filter by `ad_domain`
   - The endpoint should return a list of `AdImpression` objects

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

- **Functionality:** Does it work? Can you ingest logs and query them?
- **Correctness:** Are models, parsing, and database operations correct?
- **Code Quality:** Is the code well-structured and maintainable?
- **Problem Solving:** How do you approach debugging and error handling?

---

## Bonus Points (If time permits)

- Adding error handling (e.g., what if the S3 file doesn't exist, or a log line is malformed?)
- Making the DB session a FastAPI dependency
- Using `async/await` for I/O-bound operations

---

## Notes

- The S3 bucket is public, so you don't need AWS credentials
- Use SQLite for simplicity (no external database setup required)
- Focus on getting a working solution first, then optimize if time permits
- Check `sample.log` for example log entries

