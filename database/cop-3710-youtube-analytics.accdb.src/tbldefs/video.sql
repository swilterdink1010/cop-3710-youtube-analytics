CREATE TABLE [video] (
  [vid_id] AUTOINCREMENT CONSTRAINT [Index_2E39A056_4442_4C6E] PRIMARY KEY UNIQUE NOT NULL,
  [vid_length] LONG,
  [vid_title] VARCHAR (100),
  [vid_comments] LONG,
  [vid_upload_date] DATETIME,
  [vid_views] LONG,
  [vid_ctr] DOUBLE,
  [channel_id] LONG CONSTRAINT [fk_video_channel] REFERENCES [channel] ([channel_id]),
  [vid_likes] LONG
)
