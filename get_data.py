import pandas
import kagglehub
from kagglehub import KaggleDatasetAdapter


FILE_PATH = "./USvideos.csv"


def get_data_raw()->pandas.DataFrame:
    print("Retrieving dataset...")
    data = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "datasnaek/youtube-new",
        FILE_PATH,
    )
    return data


def main():
    raw_data = get_data_raw()
    print(raw_data[['title', 'category_id']])
    print(raw_data.columns)
    
    
if __name__ == "__main__":
    main()