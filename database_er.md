# Database Entity Relationship Diagram
![Database ER Diagram](database_er.png)

# Relational Schema
- Channel (**<u>channel_id</u>**, channel_name, channel_subs, channel_views)
- Video (**<u>vid_id</u>**, vid_length, vid_title, vid_likes, vid_comments, vid_upload_date, vid_views, vid_ctr, *channel_id*)
- Category (**<u>category_id</u>**, category_name, category_desc)
- Video Category (***<u>vid_id</u>***, ***<u>category_id</u>***)
- Category Performance (***<u>category_id</u>***, performance_ctr, performance_avg_views)
