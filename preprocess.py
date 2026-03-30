from get_data import get_data_raw
import pandas
import numpy
import os


CATEGORIES = {
    1:  ["Film & Animation",      "Content about movies, TV, and animated series"],
    2:  ["Autos & Vehicles",      "Content about cars, trucks, and other vehicles"],
    10: ["Music",                 "Music videos, performances, and audio content"],
    15: ["Pets & Animals",        "Content featuring domestic pets and wildlife"],
    17: ["Sports",                "Coverage of athletic events and sports highlights"],
    19: ["Travel & Events",       "Content about travel destinations and live events"],
    20: ["Gaming",                "Video game playthroughs, reviews, and esports"],
    22: ["People & Blogs",        "Personal vlogs and lifestyle content from creators"],
    23: ["Comedy",                "Sketches, stand-up, and humorous content"],
    24: ["Entertainment",         "General entertainment and pop culture content"],
    25: ["News & Politics",       "Current events, journalism, and political commentary"],
    26: ["Howto & Style",         "Tutorials, DIY guides, and fashion content"],
    27: ["Education",             "Educational videos and instructional content"],
    28: ["Science & Technology",  "Content about scientific topics and tech innovations"],
    29: ["Nonprofits & Activism", "Content from charitable organizations and advocacy groups"],
    43: ["Shows",                 "Content featuring episodic series, sitcoms, and television shows"],
}


def create_channel(raw_data: pandas.DataFrame)->pandas.DataFrame:
    print("Processing 'CHANNEL' table...")
    channel_subset = raw_data.drop_duplicates(subset=['channel_title']).reset_index(drop=True)
    channel = pandas.DataFrame({
        'channel_id': range(1, len(channel_subset) + 1),
        'channel_name': channel_subset['channel_title'],
        'channel_subs': numpy.random.randint(10000, 100000000, size=len(channel_subset)),
        'channel_views': numpy.random.randint(100000, 1000000000, size=len(channel_subset)),
    })
    return channel


def create_category(raw_data: pandas.DataFrame)->pandas.DataFrame:
    print("Processing 'CATEGORY' table...")
    category_subset = raw_data.drop_duplicates(subset=['category_id']).reset_index(drop=True)
    category = pandas.DataFrame({
        'category_id': category_subset['category_id'],
        'category_name': category_subset['category_id'].map(lambda x: CATEGORIES[x][0]),
        'category_desc': category_subset['category_id'].map(lambda x: CATEGORIES[x][1]),
    })
    return category


def create_video(raw_data: pandas.DataFrame, channel: pandas.DataFrame)->pandas.DataFrame:
    print("Processing 'VIDEO' table...")
    channel_lookup = channel.set_index('channel_name')['channel_id']
    video = pandas.DataFrame({
        'vid_id': range(1, len(raw_data) + 1),
        'vid_length': numpy.random.randint(120, 3600, size=len(raw_data)),
        'vid_title': raw_data['title'],
        'vid_likes': raw_data['likes'],
        'vid_comments': raw_data['comment_count'],
        'vid_upload_date': raw_data['publish_time'],
        'vid_views': raw_data['views'],
        'vid_ctr': numpy.random.uniform(0.01, 0.05, size=len(raw_data)),
        'channel_id': raw_data['channel_title'].map(channel_lookup),
    })
    return video


def create_video_category(raw_data: pandas.DataFrame, video: pandas.DataFrame)->pandas.DataFrame:
    print("Processing 'VIDEO_CATEGORY' table...")
    video_category = pandas.DataFrame({
        'vid_id': video['vid_id'],
        'category_id': raw_data['category_id'],
    })
    multiple_category_addins = []
    for _, row in video_category.iterrows():
        if numpy.random.randint(0, 3) == 0:
            addin = numpy.random.choice(list(CATEGORIES.keys()))
            if addin == row['category_id']:
                continue
            multiple_category_addins.append({
                'vid_id': row['vid_id'],
                'category_id': addin,
            })
    video_category = pandas.concat([video_category, pandas.DataFrame(multiple_category_addins)])
    return video_category


def create_category_performance(category: pandas.DataFrame, video: pandas.DataFrame, video_category: pandas.DataFrame)->pandas.DataFrame:
    print("Processing 'CATEGORY_PERFORMANCE' table...")
    video_category_merged = (
        video.merge(video_category, on='vid_id', how='inner')
             .merge(category, on='category_id', how='inner')
             .groupby('category_id')
    )
    category_performance = pandas.DataFrame({
        'category_id': category['category_id'],
        'performance_ctr': category['category_id'].map(video_category_merged['vid_ctr'].mean()),
        'performance_avg_views': category['category_id'].map(video_category_merged['vid_views'].mean()),
    })
    return category_performance


def generate_processed_data()->dict[str, pandas.DataFrame]:
    """
    Output format: channel, category, video, video_category, category_performance
    """
    raw = get_data_raw()
    channel = create_channel(raw)
    video = create_video(raw, channel)
    category = create_category(raw)
    video_category = create_video_category(raw, video)
    category_performance = create_category_performance(category, video, video_category)
    processed = {
        'channel': channel,
        'video': video,
        'category': category,
        'video_category': video_category,
        'category_performance': category_performance,
    }
    print("Processing complete.")
    return processed
    
    
def export_data(data_packed: dict[str, pandas.DataFrame])->None:
    os.makedirs("./data/", exist_ok=True)
    for name, df in data_packed.items():
        print(f"Exporting '{name}.csv'...")
        df.to_csv(f"./data/{name}.csv", index=False)
    print("Exporting complete.")
    

def main():
    packed = generate_processed_data()
    export_data(packed)


if __name__ == "__main__":
    main()