CREATE TABLE [video_category] (
  [vid_id] LONG CONSTRAINT [fk_video_category_video] REFERENCES [video] ([vid_id]),
  [category_id] LONG CONSTRAINT [fk_video_category_category] REFERENCES [category] ([category_id]),
   CONSTRAINT [pk_video_category] PRIMARY KEY ([vid_id], [category_id])
)
