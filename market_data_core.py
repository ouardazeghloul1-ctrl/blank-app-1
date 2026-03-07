from government_data_provider import load_government_data


def get_market_data(city=None, property_type=None):

    df = load_government_data()

    print("DEBUG عدد كل الصفقات:", len(df))
    print("DEBUG المدن الموجودة:", df["city"].unique()[:10])

    return df.reset_index(drop=True)
