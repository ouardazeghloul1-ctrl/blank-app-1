def generate_all_charts(self, df):
    """
    المحرك الخفي الكامل
    يولّد جميع الرسومات للفصول 1 → 8 فقط
    الفصل 9 و10 بدون رسومات (كما اتفقنا)
    """

    charts = []

    # ========= الفصل 1 =========
    charts.append(self.chapter_1_price_distribution(df))
    charts.append(self.chapter_1_price_vs_area(df))
    charts.append(self.chapter_1_future_scenarios(df))

    # ========= الفصل 2 =========
    charts.append(self.chapter_2_price_concentration(df))
    charts.append(self.chapter_2_price_volatility(df))
    charts.append(self.chapter_2_overpricing_risk(df))

    # ========= الفصل 3 =========
    charts.append(self.chapter_3_value_map(df))
    charts.append(self.chapter_3_affordable_pockets(df))
    charts.append(self.chapter_3_size_opportunities(df))

    # ========= الفصل 4 =========
    charts.append(self.chapter_4_investment_allocation_logic(df))
    charts.append(self.chapter_4_action_matrix(df))

    # ========= الفصل 5 =========
    charts.append(self.chapter_5_price_positioning(df))
    charts.append(self.chapter_5_entry_timing_signal(df))

    # ========= الفصل 6 =========
    charts.append(self.chapter_6_capital_allocation_by_risk(df))
    charts.append(self.chapter_6_capital_balance_curve(df))

    # ========= الفصل 7 =========
    charts.append(self.chapter_7_exit_pressure_zones(df))
    charts.append(self.chapter_7_hold_vs_exit_signal(df))

    # ========= الفصل 8 =========
    charts.append(self.chapter_8_anomaly_detection(df))
    charts.append(self.chapter_8_signal_intensity(df))

    return charts
