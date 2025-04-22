How to call the API

USE command 
"curl -H "Authorization: Bearer supersecrettoken123" \
     http://34.69.22.160:5000/api/capital-time/CITY_OF_YOUR_CHOICE"

Where CITY_OF_YOUR_CHOICE is the desired city
Example output for Berlin:
{
  "capital": "Berlin",
  "local_time": "2025-04-22T02:23:46+02:00",
  "utc_offset": "+02:00"
}