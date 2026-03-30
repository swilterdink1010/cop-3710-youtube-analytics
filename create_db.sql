create table channel (
    channel_id number generated always as identity primary key,
    channel_name varchar(200) not null,
    channel_subs number not null,
    channel_views number not null
);

create table video (
    vid_id number generated always as identity primary key,
    vid_length number not null,
    vid_title varchar(200) not null,
    vid_likes number,
    vid_comments number not null,
    vid_upload_date date not null,
    vid_views number not null,
    vid_ctr number(10, 9),
    channel_id number not null,
        constraint fk_video_channel
        foreign key (channel_id)
        references channel(channel_id)
);

create table category (
    category_id number generated always as identity primary key,
    category_name varchar(50) not null,
    category_desc varchar(100)
);

create table video_category (
    vid_id number not null,
        constraint fk_video_category_video
        foreign key (vid_id)
        references video(vid_id),
    category_id number not null,
        constraint fk_video_category_category
        foreign key (category_id)
        references category(category_id),
    primary key(vid_id, category_id)
);

create table category_performance (
    category_id number primary key,
        constraint fk_performance_category
        foreign key (category_id)
        references category(category_id),
    performance_ctr number(10, 9) not null,
    performance_avg_views number not null
);