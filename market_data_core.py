from government_data_provider import load_government_data


def get_market_data(city=None, property_type=None):

    df = load_government_data(selected_city=city)

    if df is None or df.empty:
        raise Exception(f"❌ لا توجد بيانات متاحة لـ {city}")

    return df.reset_index(drop=True)
