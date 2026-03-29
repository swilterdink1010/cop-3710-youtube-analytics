dbMemo "SQL" ="SELECT c.category_id, Avg(v.vid_views) AS performance_avg_views, Avg(v.vid_ctr) "
    "AS performance_ctr\015\012FROM (category AS c INNER JOIN video_category AS vc ON"
    " c.category_id = vc.category_id) INNER JOIN video AS v ON vc.vid_id = v.vid_id\015"
    "\012GROUP BY c.category_id;\015\012"
dbMemo "Connect" =""
dbBoolean "ReturnsRecords" ="-1"
dbInteger "ODBCTimeout" ="60"
dbBoolean "OrderByOn" ="0"
dbByte "Orientation" ="0"
dbByte "DefaultView" ="2"
dbBoolean "FilterOnLoad" ="0"
dbBoolean "OrderByOnLoad" ="-1"
Begin
    Begin
        dbText "Name" ="c.category_id"
        dbLong "AggregateType" ="-1"
        dbInteger "ColumnOrder" ="1"
    End
    Begin
        dbText "Name" ="performance_avg_views"
        dbInteger "ColumnWidth" ="2532"
        dbBoolean "ColumnHidden" ="0"
        dbLong "AggregateType" ="-1"
        dbInteger "ColumnOrder" ="3"
    End
    Begin
        dbText "Name" ="performance_ctr"
        dbInteger "ColumnWidth" ="1872"
        dbBoolean "ColumnHidden" ="0"
        dbLong "AggregateType" ="-1"
        dbInteger "ColumnOrder" ="2"
    End
End
