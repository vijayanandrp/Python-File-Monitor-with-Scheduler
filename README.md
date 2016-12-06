# File-Monitor-with-Scheduler
Demonstrated a simple framework to monitor the new files at the scheduled interval period.


* TO ENABLE SCHEDULE AND CONFIGURE TIMINGS [/data/etc/config.json]
```JSON
{
  "is_schedule": true,

  "schedule_time": {
    "days": 0,
    "seconds": 25,
    "microseconds": 1,
    "milliseconds": 0,
    "minutes": 0,
    "hours": 0,
    "weeks": 0
  }
}

```

