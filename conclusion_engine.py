def build_conclusion(
    strengths,
    warnings,
    cross_signals=None,
    growth_quality_evidence=None,
):
    strengths = set(strengths or [])
    warnings = set(warnings or [])
    cross_signals = set(cross_signals or [])

    growth_quality_evidence = (
        growth_quality_evidence or {}
    )

    growth_quality = (
        growth_quality_evidence.get(
            "growth_quality"
        )
    )

    conclusion_parts = []

    # ==============================
    # CORE OPERATING VIEW
    # ==============================

    if growth_quality == "recovery_breakout":
        conclusion_parts.append(
            (
                "Lợi nhuận đang phục hồi mạnh và đã vượt "
                "mức trước giai đoạn suy giảm, cho thấy "
                "quá trình cải thiện không chỉ phản ánh "
                "hiệu ứng nền thấp."
            )
        )

    elif growth_quality == "margin_driven":
        conclusion_parts.append(
            (
                "Tăng trưởng lợi nhuận hiện được thúc đẩy "
                "đáng kể bởi sự cải thiện hiệu quả sinh lời."
            )
        )

    elif "positive_growth_quality" in strengths:
        conclusion_parts.append(
            (
                "Chất lượng tăng trưởng hiện duy trì "
                "tín hiệu tương đối tích cực."
            )
        )

    else:
        conclusion_parts.append(
            (
                "Xu hướng tăng trưởng hiện chưa cho thấy "
                "một động lực nổi trội rõ ràng."
            )
        )

    # ==============================
    # OPERATING QUALITY
    # ==============================

    operating_points = []

    if (
        "strong_profitability_profile"
        in strengths
    ):
        operating_points.append(
            (
                "khả năng sinh lời và hiệu quả hoạt động "
                "đang cải thiện rõ rệt"
            )
        )

    elif "improving_profitability" in strengths:
        operating_points.append(
            (
                "hiệu quả hoạt động đang có xu hướng "
                "cải thiện"
            )
        )

    if (
        "operating_cashflow_quality_positive"
        in strengths
        or "strong_cash_conversion" in strengths
    ):
        operating_points.append(
            (
                "lợi nhuận được hỗ trợ bởi khả năng "
                "chuyển hóa thành dòng tiền tích cực"
            )
        )

    elif "operating_cashflow_positive" in strengths:
        operating_points.append(
            (
                "hoạt động kinh doanh duy trì khả năng "
                "tạo tiền"
            )
        )

    if "strong_financial_structure" in strengths:
        operating_points.append(
            (
                "cấu trúc tài chính duy trì nền tảng "
                "tương đối vững"
            )
        )

    elif "adequate_financial_structure" in strengths:
        operating_points.append(
            (
                "cấu trúc tài chính hiện vẫn ở mức "
                "tương đối cân bằng"
            )
        )

    if operating_points:
        conclusion_parts.append(
            (
                "Đồng thời, "
                + ", ".join(operating_points)
                + "."
            )
        )

    # ==============================
    # FUNDING RISK
    # ==============================

    funding_risk = None

    if (
        "persistent_fcf_deficit_with_rising_debt"
        in warnings
    ):
        funding_risk = (
            "Dòng tiền tự do âm kéo dài trong khi nợ vay "
            "gia tăng cho thấy nhu cầu đầu tư đang làm tăng "
            "mức độ phụ thuộc vào nguồn vốn bên ngoài."
        )

    elif (
        "negative_fcf_with_rising_debt"
        in warnings
    ):
        funding_risk = (
            "Dòng tiền tự do âm đi cùng xu hướng nợ vay "
            "gia tăng cho thấy nhu cầu đầu tư đang tạo "
            "thêm áp lực lên nguồn tài trợ."
        )

    elif (
        "investment_pressure_with_net_debt"
        in warnings
    ):
        funding_risk = (
            "Nhu cầu đầu tư lớn trong trạng thái nợ vay "
            "ròng cho thấy áp lực tài trợ cần tiếp tục "
            "được theo dõi."
        )

    # ==============================
    # CAPITAL PRODUCTIVITY
    # ==============================

    capital_mitigation = None

    if (
        "productive_investment_cycle"
        in strengths
        and
        "new_capital_outperforming_existing_capital_base"
        in strengths
    ):
        capital_mitigation = (
            "Tuy vậy, hiệu quả sử dụng vốn đang cải thiện "
            "và phần vốn đầu tư tăng thêm tạo ra mức sinh "
            "lời cao hơn nền vốn hiện hữu, cho thấy áp lực "
            "tài trợ hiện đi kèm với một chu kỳ đầu tư có "
            "tính sản xuất."
        )

    elif (
        "investment_pressure_with_improving_capital_productivity"
        in strengths
    ):
        capital_mitigation = (
            "Tuy vậy, hiệu quả sử dụng vốn đang cải thiện, "
            "cho thấy áp lực đầu tư hiện đi kèm với sự nâng "
            "lên của năng suất vốn."
        )

    elif (
        "investment_pressure_showing_moderation"
        in strengths
    ):
        capital_mitigation = (
            "Tuy vậy, dòng tiền hoạt động đang cải thiện "
            "và cường độ đầu tư có dấu hiệu hạ nhiệt, cho "
            "thấy áp lực tài trợ đang bắt đầu giảm."
        )

    # ==============================
    # COMBINE RISK VIEW
    # ==============================

    if funding_risk is not None:
        conclusion_parts.append(
            funding_risk
        )

    if capital_mitigation is not None:
        conclusion_parts.append(
            capital_mitigation
        )

    # ==============================
    # OTHER WARNINGS
    # ==============================

    if (
        funding_risk is None
        and "gross_margin_down" in warnings
    ):
        conclusion_parts.append(
            (
                "Tuy nhiên, xu hướng thu hẹp biên lợi nhuận "
                "gộp cần tiếp tục được theo dõi."
            )
        )

    # ==============================
    # FINAL CONCLUSION
    # ==============================

    return " ".join(conclusion_parts)