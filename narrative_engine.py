def build_narratives(
    strengths,
    warnings,
    margin_evidence,
    growth_evidence=None,
    cashflow_evidence=None,
    balance_evidence=None,
    growth_quality_evidence=None,
    capital_efficiency_evidence=None,
):
    
    strengths = set(strengths or [])
    warnings = set(warnings or [])

    margin_evidence = margin_evidence or {}
    growth_evidence = growth_evidence or {}
    cashflow_evidence = cashflow_evidence or {}
    balance_evidence = balance_evidence or {}
    growth_quality_evidence = growth_quality_evidence or {}
    capital_efficiency_evidence = (
        capital_efficiency_evidence or {}
    )

    analysis = []


    # ==============================
    # EVIDENCE OBJECTS
    # ==============================

    revenue = growth_evidence.get(
        "revenue",
        {},
    )

    profit = growth_evidence.get(
        "profit",
        {},
    )

    profit_vs_revenue = growth_evidence.get(
        "profit_vs_revenue",
        {},
    )

    gross_margin = margin_evidence.get(
        "gross_margin",
        {},
    )

    operating_margin = margin_evidence.get(
        "operating_margin",
        {},
    )

    operating_cashflow = cashflow_evidence.get(
        "operating_cashflow",
        {},
    )

    capex = cashflow_evidence.get(
        "capex",
        {},
    )

    free_cashflow = cashflow_evidence.get(
        "free_cashflow",
        {},
    )

    cash_conversion = cashflow_evidence.get(
        "cash_conversion",
        {},
    )

    # ==============================
    # 1. REVENUE TREND
    # ==============================

    if revenue:
        analysis.append(
            "Doanh thu mở rộng từ "
            f"{revenue.get('first_text', 'N/A')} "
            f"năm {revenue.get('first_year', 'N/A')} "
            "lên "
            f"{revenue.get('current_text', 'N/A')} "
            f"năm {revenue.get('latest_year', 'N/A')}."
        )

    # ==============================
    # 2. RECENT GROWTH
    # ==============================

    revenue_growth = revenue.get(
        "growth"
    )

    profit_growth = profit.get(
        "growth"
    )

    difference = profit_vs_revenue.get(
        "difference"
    )

    if (
        revenue_growth is not None
        and profit_growth is not None
    ):
        if (
            difference is not None
            and difference > 0
        ):
            analysis.append(
                "Trong kỳ gần nhất, doanh thu tăng "
                f"{revenue.get('growth_text', 'N/A')}, "
                "trong khi lợi nhuận tăng "
                f"{profit.get('growth_text', 'N/A')}, "
                "cao hơn "
                f"{profit_vs_revenue.get('difference_text', 'N/A')}, "
                "cho thấy lợi nhuận đang tăng nhanh hơn doanh thu."
            )

        elif (
            difference is not None
            and difference < 0
        ):
            analysis.append(
                "Trong kỳ gần nhất, doanh thu tăng "
                f"{revenue.get('growth_text', 'N/A')}, "
                "trong khi lợi nhuận tăng "
                f"{profit.get('growth_text', 'N/A')}, "
                "thấp hơn tốc độ tăng doanh thu "
                f"{abs(difference):.2f} điểm %, "
                "cho thấy khả năng chuyển hóa tăng trưởng doanh thu "
                "thành lợi nhuận đang chịu áp lực."
            )

        else:
            analysis.append(
                "Trong kỳ gần nhất, doanh thu tăng "
                f"{revenue.get('growth_text', 'N/A')}, "
                "và lợi nhuận tăng "
                f"{profit.get('growth_text', 'N/A')}, "
                "cho thấy tốc độ tăng trưởng lợi nhuận "
                "gần tương đồng với doanh thu."
            )

    # ==============================
    # 3. GROWTH QUALITY
    # ==============================

    growth_quality = (
        growth_quality_evidence.get(
            "growth_quality"
        )
    )

    growth_quality_diagnostics = (
        growth_quality_evidence.get(
            "diagnostics",
            {},
        )
    )

    if growth_quality == "recovery_breakout":
        trough_year = (
            growth_quality_diagnostics.get(
                "trough_year"
            )
        )

        recovery_above_pre_trough = (
            growth_quality_diagnostics.get(
                "recovery_above_pre_trough"
            )
        )

        if (
            trough_year is not None
            and recovery_above_pre_trough
        ):
            analysis.append(
                (
                    f"Lợi nhuận đang trong pha phục hồi "
                    f"mạnh sau đáy năm {trough_year}. "
                    f"Mức lợi nhuận hiện tại đã vượt "
                    f"mức trước giai đoạn suy giảm, "
                    f"cho thấy đà tăng không chỉ phản ánh "
                    f"hiệu ứng nền thấp mà còn đi kèm "
                    f"sự phục hồi thực của khả năng sinh lời."
                )
            )

    elif growth_quality == "structural_growth":
        analysis.append(
            (
                "Tăng trưởng lợi nhuận đang được hỗ trợ "
                "bởi xu hướng mở rộng hoạt động kinh doanh "
                "mang tính dài hạn. Diễn biến này cho thấy "
                "động lực tăng trưởng có tính cấu trúc "
                "thay vì chỉ đến từ biến động ngắn hạn."
            )
        )

    elif growth_quality == "low_base_recovery":
        trough_year = (
            growth_quality_diagnostics.get(
                "trough_year"
            )
        )

        if trough_year is not None:
            analysis.append(
                (
                    f"Lợi nhuận đang phục hồi từ mức nền "
                    f"thấp sau đáy năm {trough_year}. "
                    f"Tốc độ tăng trưởng hiện tại cần được "
                    f"đánh giá thận trọng do một phần có thể "
                    f"phản ánh hiệu ứng nền thấp của kỳ trước."
                )
            )

    elif growth_quality == "margin_driven":
        analysis.append(
            (
                "Tăng trưởng lợi nhuận hiện được hỗ trợ "
                "đáng kể bởi sự cải thiện hiệu quả sinh lời "
                "và kiểm soát chi phí. Động lực tăng trưởng "
                "đến nhiều hơn từ biên lợi nhuận thay vì "
                "sự mở rộng mạnh của doanh thu."
            )
        )

    # ==============================
    # 3. GROSS MARGIN
    # ==============================

    gross_margin_change = gross_margin.get(
        "change"
    )

    if gross_margin_change is not None:
        if gross_margin_change > 0:
            analysis.append(
                "Biên lợi nhuận gộp tăng từ "
                f"{gross_margin.get('first_text', 'N/A')} "
                "lên "
                f"{gross_margin.get('current_text', 'N/A')}, "
                "tương ứng "
                f"{gross_margin.get('change_text', 'N/A')}. "
                "Diễn biến này cho thấy khả năng tạo lợi nhuận "
                "trên doanh thu đang được cải thiện."
            )

        elif gross_margin_change < 0:
            analysis.append(
                "Biên lợi nhuận gộp giảm từ "
                f"{gross_margin.get('first_text', 'N/A')} "
                "xuống "
                f"{gross_margin.get('current_text', 'N/A')}, "
                "tương ứng "
                f"{gross_margin.get('change_text', 'N/A')}, "
                "cho thấy biên lợi nhuận gộp đang chịu áp lực."
            )

    # ==============================
    # 4. OPERATING MARGIN
    # ==============================

    operating_margin_change = operating_margin.get(
        "change"
    )

    if operating_margin_change is not None:
        if operating_margin_change > 0:
            analysis.append(
                "Biên lợi nhuận hoạt động tăng từ "
                f"{operating_margin.get('first_text', 'N/A')} "
                "lên "
                f"{operating_margin.get('current_text', 'N/A')}, "
                "cho thấy hiệu quả hoạt động đang được cải thiện."
            )

        elif operating_margin_change < 0:
            analysis.append(
                "Biên lợi nhuận hoạt động giảm từ "
                f"{operating_margin.get('first_text', 'N/A')} "
                "xuống "
                f"{operating_margin.get('current_text', 'N/A')}, "
                "cho thấy hiệu quả hoạt động đang chịu áp lực."
            )

    # ==============================
    # 5. MARGIN DIVERGENCE
    # ==============================

    if (
        gross_margin_change is not None
        and operating_margin_change is not None
        and gross_margin_change < 0
        and operating_margin_change > 0
    ):
        analysis.append(
            "Mặc dù biên lợi nhuận gộp đang thu hẹp, "
            "biên lợi nhuận hoạt động vẫn cải thiện. "
            "Diễn biến này cho thấy hiệu quả vận hành và "
            "kiểm soát chi phí đang bù đắp một phần áp lực "
            "tại cấp độ lợi nhuận gộp."
        )

    # ==============================
    # 6. CASH FLOW
    # ==============================

    operating_cashflow_value = (
        operating_cashflow.get(
            "current"
        )
    )

    free_cashflow_value = (
        free_cashflow.get(
            "current"
        )
    )

    capex_value = capex.get(
        "current"
    )

    if (
        operating_cashflow_value is not None
        and free_cashflow_value is not None
    ):
        if free_cashflow_value > 0:
            analysis.append(
                "Dòng tiền từ hoạt động kinh doanh đạt "
                f"{operating_cashflow.get('current_text', 'N/A')}. "
                "Sau nhu cầu đầu tư tài sản dài hạn, doanh nghiệp "
                "vẫn tạo ra "
                f"{free_cashflow.get('current_text', 'N/A')} "
                "dòng tiền tự do dương, cho thấy hoạt động kinh doanh "
                "có khả năng tạo tiền và hỗ trợ nhu cầu đầu tư."
            )

        elif free_cashflow_value < 0:
            capex_text = capex.get(
                "current_text",
                "N/A",
            )

            if (
                capex_value is not None
                and capex_value < 0
            ):
                capex_text = (
                    capex_text.replace(
                        "-",
                        "",
                    )
                )

            analysis.append(
                "Dòng tiền từ hoạt động kinh doanh đạt "
                f"{operating_cashflow.get('current_text', 'N/A')}, "
                "trong khi chi đầu tư tài sản dài hạn ở mức "
                f"{capex_text}. "
                "Do nhu cầu đầu tư vượt dòng tiền tạo ra từ "
                "hoạt động kinh doanh, dòng tiền tự do ghi nhận "
                f"{free_cashflow.get('current_text', 'N/A')}. "
                "Diễn biến này cho thấy doanh nghiệp đang có "
                "cường độ đầu tư vốn lớn."
            )

    # ==============================
    # 7. CASH CONVERSION
    # ==============================

    cash_conversion_value = (
        cash_conversion.get(
            "current"
        )
    )

    if cash_conversion_value is not None:
        if cash_conversion_value >= 1:
            analysis.append(
                "Tỷ lệ chuyển đổi dòng tiền từ hoạt động kinh doanh "
                "so với lợi nhuận đạt "
                f"{cash_conversion.get('current_text', 'N/A')}. "
                "Điều này cho thấy lợi nhuận kế toán được chuyển hóa "
                "thành dòng tiền thực ở mức tích cực, hỗ trợ "
                "chất lượng lợi nhuận."
            )

        elif cash_conversion_value >= 0.8:
            analysis.append(
                "Tỷ lệ chuyển đổi dòng tiền từ hoạt động kinh doanh "
                "so với lợi nhuận đạt "
                f"{cash_conversion.get('current_text', 'N/A')}. "
                "Khả năng chuyển hóa lợi nhuận thành dòng tiền "
                "đang ở mức tương đối tích cực."
            )

        elif cash_conversion_value > 0:
            analysis.append(
                "Tỷ lệ chuyển đổi dòng tiền từ hoạt động kinh doanh "
                "so với lợi nhuận đạt "
                f"{cash_conversion.get('current_text', 'N/A')}. "
                "Mức chuyển đổi dòng tiền còn tương đối thấp và "
                "cần tiếp tục được theo dõi."
            )

    # ==============================
    # 8. FINANCIAL STRUCTURE
    # ==============================

    total_debt = balance_evidence.get(
        "total_debt",
        {},
    )

    net_debt = balance_evidence.get(
        "net_debt",
        {},
    )

    debt_to_equity = balance_evidence.get(
        "debt_to_equity",
        {},
    )

    equity_to_assets = balance_evidence.get(
        "equity_to_assets",
        {},
    )

    debt_change = balance_evidence.get(
        "debt_change",
        {},
    )

    total_debt_value = total_debt.get(
        "current"
    )

    net_debt_value = net_debt.get(
        "current"
    )

    debt_to_equity_value = debt_to_equity.get(
        "current"
    )

    equity_to_assets_value = equity_to_assets.get(
        "current"
    )

    debt_change_value = debt_change.get(
        "current"
    )

    # ==============================
    # FINANCIAL LEVERAGE JUDGMENT
    # ==============================

    if (
        total_debt_value is not None
        and debt_to_equity_value is not None
        and equity_to_assets_value is not None
    ):
        if debt_to_equity_value < 0.5:
            analysis.append(
                "Tổng nợ vay hiện ở mức "
                f"{total_debt.get('current_text', 'N/A')}, "
                "tương đương "
                f"{debt_to_equity.get('current_text', 'N/A')} "
                "vốn chủ sở hữu. "
                "Doanh nghiệp đang duy trì mức đòn bẩy tài chính thấp, "
                "trong khi vốn chủ sở hữu chiếm "
                f"{equity_to_assets.get('current_text', 'N/A')} "
                "tổng tài sản. "
                "Cấu trúc vốn tương đối thận trọng và vẫn còn "
                "dư địa sử dụng nguồn vốn vay khi cần thiết."
            )

        elif debt_to_equity_value < 1.0:
            analysis.append(
                "Tổng nợ vay hiện ở mức "
                f"{total_debt.get('current_text', 'N/A')}, "
                "tương đương "
                f"{debt_to_equity.get('current_text', 'N/A')} "
                "vốn chủ sở hữu. "
                "Doanh nghiệp đang sử dụng đòn bẩy tài chính "
                "ở mức trung bình, trong khi vốn chủ sở hữu chiếm "
                f"{equity_to_assets.get('current_text', 'N/A')} "
                "tổng tài sản. "
                "Cấu trúc vốn hiện chưa cho thấy áp lực đòn bẩy "
                "quá lớn, nhưng dư địa tài chính không còn ở mức "
                "đặc biệt thận trọng."
            )

        else:
            analysis.append(
                "Tổng nợ vay hiện ở mức "
                f"{total_debt.get('current_text', 'N/A')}, "
                "tương đương "
                f"{debt_to_equity.get('current_text', 'N/A')} "
                "vốn chủ sở hữu. "
                "Mức đòn bẩy tài chính hiện tương đối cao, "
                "cho thấy doanh nghiệp đang phụ thuộc đáng kể "
                "vào nguồn vốn vay. "
                "Cấu trúc này có thể làm gia tăng độ nhạy của "
                "lợi nhuận và dòng tiền trước biến động lãi suất "
                "hoặc suy giảm hoạt động kinh doanh."
            )

    # ==============================
    # DEBT TREND
    # ==============================

    if (
        net_debt_value is not None
        and debt_change_value is not None
    ):
        if debt_change_value > 15:
            analysis.append(
                "Doanh nghiệp đang duy trì vị thế nợ ròng "
                f"{net_debt.get('current_text', 'N/A')}, "
                "trong khi tổng nợ vay tăng "
                f"{debt_change.get('current_text', 'N/A')} "
                "so với kỳ trước. "
                "Xu hướng gia tăng nợ vay cần được theo dõi cùng "
                "khả năng tạo dòng tiền và nhu cầu đầu tư vốn "
                "trong các kỳ tiếp theo."
            )

        elif debt_change_value < -15:
            analysis.append(
                "Doanh nghiệp đang duy trì vị thế nợ ròng "
                f"{net_debt.get('current_text', 'N/A')}, "
                "nhưng tổng nợ vay đã giảm "
                f"{abs(debt_change_value):.2f}% "
                "so với kỳ trước. "
                "Diễn biến này cho thấy áp lực từ nguồn vốn vay "
                "đang có xu hướng được thu hẹp."
            )

    # ==============================
    # CAPITAL EFFICIENCY NARRATIVE
    # ==============================

    if capital_efficiency_evidence:
        latest_roic = (
            capital_efficiency_evidence.get(
                "latest_roic"
            )
        )

        previous_roic = (
            capital_efficiency_evidence.get(
                "previous_roic"
            )
        )

        roic_change = (
            capital_efficiency_evidence.get(
                "roic_change"
            )
        )

        incremental_roic = (
            capital_efficiency_evidence.get(
                "incremental_roic"
            )
        )

        capital_efficiency_regime = (
            capital_efficiency_evidence.get(
                "capital_efficiency_regime"
            )
        )

        capital_signals = set(
            capital_efficiency_evidence.get(
                "signals",
                [],
            )
        )

        # ==========================
        # ROIC TREND
        # ==========================

        if (
            latest_roic is not None
            and previous_roic is not None
        ):
            if latest_roic > previous_roic:
                analysis.append(
                    (
                        "ROIC tăng từ "
                        f"{previous_roic * 100:.2f}% "
                        "lên "
                        f"{latest_roic * 100:.2f}%, "
                        "cho thấy hiệu quả sinh lời "
                        "trên phần vốn đầu tư đang "
                        "được cải thiện."
                    )
                )

            elif latest_roic < previous_roic:
                analysis.append(
                    (
                        "ROIC giảm từ "
                        f"{previous_roic * 100:.2f}% "
                        "xuống "
                        f"{latest_roic * 100:.2f}%, "
                        "cho thấy hiệu quả sinh lời "
                        "trên phần vốn đầu tư đang "
                        "chịu áp lực."
                    )
                )

            else:
                analysis.append(
                    (
                        "ROIC duy trì ở mức "
                        f"{latest_roic * 100:.2f}%, "
                        "cho thấy hiệu quả sử dụng "
                        "vốn chưa có thay đổi đáng kể "
                        "so với kỳ trước."
                    )
                )

        # ==========================
        # INCREMENTAL ROIC
        # ==========================

        if (
            incremental_roic is not None
            and latest_roic is not None
        ):
            if (
                incremental_roic
                > latest_roic
            ):
                analysis.append(
                    (
                        "Incremental ROIC đạt "
                        f"{incremental_roic * 100:.2f}%, "
                        "cao hơn ROIC hiện tại ở mức "
                        f"{latest_roic * 100:.2f}%. "
                        "Diễn biến này cho thấy phần "
                        "vốn đầu tư tăng thêm đang tạo "
                        "ra mức sinh lời cao hơn nền "
                        "vốn hiện hữu, hỗ trợ sự cải "
                        "thiện năng suất sử dụng vốn."
                    )
                )

            elif incremental_roic > 0:
                analysis.append(
                    (
                        "Incremental ROIC đạt "
                        f"{incremental_roic * 100:.2f}%, "
                        "thấp hơn ROIC hiện tại ở mức "
                        f"{latest_roic * 100:.2f}%. "
                        "Phần vốn đầu tư tăng thêm vẫn "
                        "tạo ra lợi nhuận, nhưng hiệu "
                        "quả hiện thấp hơn nền vốn "
                        "hiện hữu."
                    )
                )

            else:
                analysis.append(
                    (
                        "Incremental ROIC ở mức "
                        f"{incremental_roic * 100:.2f}%. "
                        "Hiệu quả của phần vốn đầu tư "
                        "tăng thêm đang ở trạng thái "
                        "yếu và có thể tạo áp lực lên "
                        "năng suất vốn tổng thể."
                    )
                )

        # ==========================
        # CAPITAL REGIME
        # ==========================


        elif (
            capital_efficiency_regime
            == "improving_capital_efficiency"
        ):
            analysis.append(
                (
                    "Hiệu quả sử dụng vốn đang có "
                    "xu hướng cải thiện, cho thấy "
                    "doanh nghiệp đang tạo ra mức "
                    "sinh lời tốt hơn trên nền vốn "
                    "đầu tư."
                )
            )

        elif (
            capital_efficiency_regime
            == "weak_incremental_returns"
        ):
            analysis.append(
                (
                    "Hiệu quả của phần vốn đầu tư "
                    "tăng thêm đang thấp hơn nền vốn "
                    "hiện hữu. Nếu xu hướng này kéo "
                    "dài, hiệu quả sử dụng vốn tổng "
                    "thể có thể chịu áp lực."
                )
            )

        elif (
            capital_efficiency_regime
            == "negative_incremental_returns"
        ):
            analysis.append(
                (
                    "Phần vốn đầu tư tăng thêm hiện "
                    "chưa tạo ra lợi nhuận tương ứng. "
                    "Diễn biến này cho thấy rủi ro "
                    "phân bổ vốn cần được theo dõi "
                    "chặt chẽ."
                )
            )

    return analysis