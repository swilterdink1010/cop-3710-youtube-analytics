CREATE TABLE [category_performance] (
  [category_id] LONG CONSTRAINT [fk_category_performance_category] REFERENCES [category] ([category_id]) CONSTRAINT [Index_8FD03215_8D82_4CB8] PRIMARY KEY UNIQUE NOT NULL,
  [performance_ctr] DOUBLE,
  [performance_avg_views] LONG
)
