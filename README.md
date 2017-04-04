# Manipal Attendance Claims
### API Documentation
## /classdata
**Method** : GET <br>
**Description**: To get the classes scheduled by default for a particular date and batch.  

| Parameters|Values|
| ----------|------|
| date|**string** <br>Format: YYYY-MM-DD<br>Eg: 2017-16-12|
|batch|**string**<br> Choose between batch_a and batch_b|

**Example** : <br> Request: http://localhost:5000/classdata?date=2017-06-16&batch=batch_a<br>
Response:<br>{<br>
  "2 PM to 3 PM": "Pathology",<br>
  "3 PM to 4 PM": "Community Medicine practicals",<br>
  "4 PM to 5 PM": NaN, <br>
  "8 AM to 9 AM": "Surgery",<br>
  "9:30 AM to 12 Noon": "Postings"<br>
}
