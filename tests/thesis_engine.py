# ============================================================
# THESIS ENGINE
# ============================================================


def _get_signals(
    result,
):
    if (
        result is None
        or not isinstance(
            result,
            dict,
        )
        or result.get(
            "status"
        )
        != "success"
    ):
        return set()

    return set(
        result.get(
            "signals",
            [],
        )
    )


# ============================================================
# BUILD GROWTH DRIVER
# ============================================================


def build_growth_driver(
    earnings_driver_result,
):
    if (
        earnings_driver_result is None
        or earnings_driver_result.get(
            "status"
        )
        != "success"
    ):
        return (
            "Động lực tăng trưởng lợi nhuận "
            "hiện chưa được xác định rõ từ "
            "các dữ liệu phân tích hiện có."
        )

    growth_regime = (
        earnings_driver_result.get(
            "growth_regime"
        )
    )

    driver_profile = (
        earnings_driver_result.get(
            "driver_profile"
        )
    )

    primary_drivers = set(
        earnings_driver_result.get(
            "primary_drivers",
            [],
        )
    )

    secondary_drivers = set(
        earnings_driver_result.get(
            "secondary_drivers",
            [],
        )
    )

    mechanisms = set(
        earnings_driver_result.get(
            "earnings_mechanism",
            [],
        )
    )

    offsets = set(
        earnings_driver_result.get(
            "offset_factors",
            [],
        )
    )

    # ========================================================
    # MARGIN DRIVEN
    # ========================================================

    if (
        growth_regime
        == "margin_driven"
        or driver_profile
        == "margin_driven"
    ):
        if (
            "gross_margin_expansion"
            in primary_drivers
        ):
            if (
                "revenue_expansion"
                in secondary_drivers
            ):
                return (
                    "Động lực tăng trưởng lợi nhuận "
                    "hiện chủ yếu đến từ sự cải thiện "
                    "biên lợi nhuận gộp, trong khi "
                    "tăng trưởng doanh thu đóng vai trò "
                    "hỗ trợ. Khả năng tạo lợi nhuận trên "
                    "doanh thu đang được nâng lên và trở "
                    "thành yếu tố chính thúc đẩy kết quả "
                    "kinh doanh."
                )

            return (
                "Động lực tăng trưởng lợi nhuận "
                "hiện chủ yếu đến từ sự cải thiện "
                "biên lợi nhuận gộp. Khả năng tạo "
                "lợi nhuận trên doanh thu đang được "
                "nâng lên và đóng vai trò chính trong "
                "quá trình cải thiện kết quả kinh doanh."
            )

    # ========================================================
    # REVENUE AND EFFICIENCY DRIVEN
    # ========================================================

    if (
        driver_profile
        == "revenue_and_efficiency_driven"
    ):
        if (
            "revenue_expansion"
            in primary_drivers
            and "selling_efficiency"
            in primary_drivers
        ):
            return (
                "Động lực tăng trưởng lợi nhuận "
                "hiện đến từ sự kết hợp giữa mở rộng "
                "doanh thu và cải thiện hiệu quả chi phí "
                "bán hàng. Doanh thu tăng tạo nền tảng "
                "tăng trưởng, trong khi tỷ trọng chi phí "
                "bán hàng giảm giúp doanh nghiệp chuyển hóa "
                "tăng trưởng doanh thu thành mức tăng lợi "
                "nhuận cao hơn."
            )

    # ========================================================
    # REVENUE DRIVEN
    # ========================================================

    if (
        "revenue_expansion"
        in primary_drivers
    ):
        if (
            "operating_leverage"
            in mechanisms
        ):
            return (
                "Động lực tăng trưởng lợi nhuận "
                "hiện chủ yếu đến từ sự mở rộng doanh thu. "
                "Quy mô hoạt động tăng đang tạo hiệu ứng "
                "đòn bẩy hoạt động, giúp lợi nhuận tăng "
                "nhanh hơn tốc độ tăng doanh thu."
            )

        return (
            "Động lực tăng trưởng lợi nhuận "
            "hiện chủ yếu đến từ sự mở rộng doanh thu. "
            "Tăng trưởng quy mô kinh doanh đang đóng vai "
            "trò chính trong quá trình cải thiện kết quả "
            "lợi nhuận."
        )

    # ========================================================
    # EFFICIENCY DRIVEN
    # ========================================================

    if (
        "selling_efficiency"
        in primary_drivers
        or "admin_efficiency"
        in primary_drivers
    ):
        return (
            "Động lực tăng trưởng lợi nhuận "
            "hiện chủ yếu đến từ sự cải thiện hiệu quả "
            "chi phí hoạt động. Khả năng kiểm soát chi phí "
            "đang giúp doanh nghiệp chuyển hóa doanh thu "
            "thành lợi nhuận hiệu quả hơn."
        )

    # ========================================================
    # PRESSURE / MIXED
    # ========================================================

    if offsets:
        return (
            "Động lực tăng trưởng lợi nhuận hiện mang "
            "tính hỗn hợp. Một số yếu tố vận hành đang "
            "hỗ trợ kết quả kinh doanh, nhưng vẫn tồn tại "
            "các áp lực có thể hạn chế tốc độ cải thiện "
            "lợi nhuận."
        )

    return (
        "Động lực tăng trưởng lợi nhuận "
        "hiện có tín hiệu tích cực, nhưng chưa có "
        "một yếu tố đơn lẻ đủ nổi bật để xác định "
        "là động lực tăng trưởng chính."
    )


# ============================================================
# BUILD GROWTH QUALITY
# ============================================================


def build_growth_quality_view(
    growth_quality_evidence,
):
    if not growth_quality_evidence:
        return (
            "Chất lượng tăng trưởng hiện chưa có đủ "
            "dữ liệu để đánh giá đầy đủ."
        )

    growth_quality = (
        growth_quality_evidence.get(
            "growth_quality"
        )
    )

    signals = set(
        growth_quality_evidence.get(
            "signals",
            [],
        )
    )

    diagnostics = (
        growth_quality_evidence.get(
            "diagnostics",
            {},
        )
    )

    profit_history = (
        growth_quality_evidence.get(
            "profit_history",
            [],
        )
    )

    # ========================================================
    # PROFIT DETERIORATION
    # HIGHEST PRIORITY
    # ========================================================

    latest_profit = diagnostics.get(
        "latest_profit"
    )

    previous_profit = diagnostics.get(
        "previous_profit"
    )

    if (
        latest_profit is not None
        and previous_profit is not None
        and previous_profit > 0
        and latest_profit < previous_profit
    ):
        profit_change = (
            latest_profit
            / previous_profit
            - 1
        )

        if profit_change <= -0.30:
            return (
                "Chất lượng tăng trưởng đang suy yếu rõ rệt khi "
                "lợi nhuận kỳ gần nhất giảm mạnh so với kỳ trước. "
                "Diễn biến này cho thấy doanh nghiệp chưa duy trì "
                "được động lực tăng trưởng lợi nhuận và khả năng "
                "sinh lời đang chịu áp lực đáng kể."
            )

        return (
            "Chất lượng tăng trưởng đang chịu áp lực khi lợi "
            "nhuận kỳ gần nhất suy giảm so với kỳ trước. Khả năng "
            "ổn định và phục hồi lợi nhuận cần được theo dõi trong "
            "các kỳ tiếp theo."
        )

    # ========================================================
    # PERSISTENT PROFIT WEAKNESS
    # ========================================================

    if len(
        profit_history
    ) >= 3:
        recent_profits = [
            item.get(
                "profit"
            )
            for item in profit_history[-3:]
            if item.get(
                "profit"
            )
            is not None
        ]

        if (
            len(recent_profits) == 3
            and recent_profits[0]
            > recent_profits[1]
            > recent_profits[2]
        ):
            return (
                "Chất lượng tăng trưởng đang suy yếu khi lợi "
                "nhuận giảm liên tiếp trong các kỳ gần đây. Xu "
                "hướng này cho thấy khả năng tạo lợi nhuận chưa "
                "ổn định và động lực tăng trưởng đang suy giảm."
            )

    # ========================================================
    # RECOVERY BREAKOUT
    # ========================================================

    if (
        growth_quality
        == "recovery_breakout"
    ):
        if diagnostics.get(
            "recovery_above_pre_trough"
        ):
            return (
                "Chất lượng phục hồi lợi nhuận có tín hiệu "
                "tích cực do lợi nhuận đã vượt mức trước "
                "giai đoạn suy giảm. Điều này cho thấy đà "
                "tăng không chỉ phản ánh hiệu ứng nền thấp "
                "mà còn đi kèm sự phục hồi thực của khả năng "
                "sinh lời."
            )

        return (
            "Lợi nhuận đang trong pha phục hồi mạnh sau "
            "giai đoạn suy giảm. Chất lượng tăng trưởng "
            "được cải thiện, dù vẫn cần theo dõi khả năng "
            "duy trì mức lợi nhuận sau quá trình phục hồi."
        )

    # ========================================================
    # MARGIN DRIVEN
    # ========================================================

    if (
        growth_quality
        == "margin_driven"
    ):
        if (
            "margin_driven_profit_growth"
            in signals
        ):
            return (
                "Chất lượng tăng trưởng hiện có tín hiệu "
                "tích cực do lợi nhuận được hỗ trợ trực tiếp "
                "bởi sự mở rộng biên lợi nhuận gộp. Việc "
                "biên lợi nhuận hoạt động đồng thời cải thiện "
                "cho thấy khả năng sinh lời đang được nâng lên "
                "trên nền hoạt động cốt lõi."
            )

        return (
            "Tăng trưởng lợi nhuận hiện được hỗ trợ đáng kể "
            "bởi sự cải thiện biên lợi nhuận. Chất lượng tăng "
            "trưởng có tín hiệu tích cực, nhưng cần tiếp tục "
            "theo dõi khả năng duy trì mức biên lợi nhuận mới."
        )

    # ========================================================
    # REVENUE DRIVEN
    # ========================================================

    if (
        growth_quality
        == "revenue_driven"
    ):
        return (
            "Chất lượng tăng trưởng hiện chủ yếu dựa trên "
            "sự mở rộng doanh thu. Điều này cho thấy tăng "
            "trưởng đang được hỗ trợ bởi quy mô hoạt động, "
            "dù khả năng chuyển hóa doanh thu thành lợi nhuận "
            "vẫn cần được theo dõi."
        )

    # ========================================================
    # STRONG PROFIT QUALITY
    # ========================================================

    if (
        "strong_profit_growth_quality"
        in signals
    ):
        return (
            "Chất lượng tăng trưởng lợi nhuận hiện có tín hiệu "
            "tích cực khi lợi nhuận tăng nhanh hơn doanh thu. "
            "Diễn biến này cho thấy khả năng chuyển hóa tăng "
            "trưởng hoạt động thành lợi nhuận đang được cải thiện."
        )

    # ========================================================
    # DEFAULT
    # ========================================================

    return (
        "Chất lượng tăng trưởng hiện chưa hình thành xu hướng "
        "đủ rõ để đưa ra đánh giá tích cực hoặc tiêu cực độc lập."
    )


# ============================================================
# BUILD CAPITAL QUALITY
# ============================================================


def build_capital_quality_view(
    capital_efficiency_result,
    capital_allocation_result,
):
    efficiency_signals = _get_signals(
        capital_efficiency_result
    )

    allocation_signals = _get_signals(
        capital_allocation_result
    )

    # ========================================================
    # DESTRUCTIVE CAPITAL DEPLOYMENT
    # HIGHEST PRIORITY
    # ========================================================

    if (
        "incremental_capital_value_destructive"
        in efficiency_signals
        or "negative_incremental_roic"
        in efficiency_signals
    ):
        if (
            "roic_deteriorating"
            in efficiency_signals
        ):
            return (
                "Hiệu quả sử dụng vốn đang suy giảm rõ rệt. "
                "ROIC tiếp tục đi xuống trong khi phần vốn đầu tư "
                "tăng thêm tạo ra mức sinh lời âm, cho thấy vốn "
                "mới chưa tạo ra lợi nhuận vận hành tương xứng. "
                "Diễn biến này phản ánh chất lượng phân bổ vốn "
                "đang chịu áp lực và phần vốn tăng thêm hiện có "
                "dấu hiệu làm suy giảm năng suất vốn tổng thể."
            )

        return (
            "Phần vốn đầu tư tăng thêm đang tạo ra mức sinh lời "
            "âm, cho thấy hiệu quả sử dụng vốn mới ở trạng thái "
            "yếu. Nếu xu hướng này kéo dài, quá trình tái đầu tư "
            "có thể tiếp tục gây áp lực lên năng suất vốn tổng thể."
        )

    # ========================================================
    # DETERIORATING CAPITAL EFFICIENCY
    # ========================================================

    if (
        "roic_deteriorating"
        in efficiency_signals
    ):
        return (
            "Hiệu quả sinh lời trên vốn đầu tư đang suy giảm. "
            "Xu hướng ROIC đi xuống cho thấy năng suất của nền "
            "vốn hiện hữu đang chịu áp lực và cần được theo dõi "
            "trong các kỳ tiếp theo."
        )

    # ========================================================
    # STRONG PRODUCTIVE REINVESTMENT
    # ========================================================

    if (
        "strong_incremental_returns"
        in allocation_signals
        and "new_capital_more_productive"
        in allocation_signals
        and "profit_growth_outpaces_capital_growth"
        in allocation_signals
    ):
        return (
            "Hiệu quả sinh lời trên nền vốn hiện hữu vẫn ở mức "
            "thấp. Tuy nhiên, ROIC đang cải thiện và phần vốn đầu "
            "tư tăng thêm đang tạo ra mức sinh lời cao hơn đáng "
            "kể so với nền vốn hiện tại. Đồng thời, tốc độ tăng "
            "NOPAT đang vượt tốc độ mở rộng vốn đầu tư, cho thấy "
            "quá trình tái đầu tư hiện có dấu hiệu nâng cao năng "
            "suất sử dụng vốn."
        )

    # ========================================================
    # IMPROVING CAPITAL PRODUCTIVITY
    # ========================================================

    if (
        "capital_productivity_recovery"
        in efficiency_signals
        or (
            "incremental_capital_materially_more_productive"
            in efficiency_signals
        )
    ):
        return (
            "Hiệu quả sử dụng vốn đang có dấu hiệu cải thiện. "
            "Phần vốn đầu tư tăng thêm đang tạo ra mức sinh lời "
            "cao hơn nền vốn hiện hữu, cho thấy năng suất của "
            "vốn mới đang hỗ trợ quá trình phục hồi hiệu quả vốn."
        )

    # ========================================================
    # MATURE HIGH RETURN BUSINESS
    # ========================================================

    allocation_regime = None
    efficiency_regime = None
    efficiency_profile = None
    latest_roic = None

    if (
        capital_allocation_result is not None
        and isinstance(
            capital_allocation_result,
            dict,
        )
    ):
        allocation_regime = (
            capital_allocation_result.get(
                "allocation_regime"
            )
        )

    if (
        capital_efficiency_result is not None
        and isinstance(
            capital_efficiency_result,
            dict,
        )
    ):
        efficiency_regime = (
            capital_efficiency_result.get(
                "capital_efficiency_regime"
            )
        )

        efficiency_profile = (
            capital_efficiency_result.get(
                "capital_efficiency_profile"
            )
        )

        latest_roic = (
            capital_efficiency_result.get(
                "latest_roic"
            )
        )

    if (
        allocation_regime
        == "mature_high_return_business"
    ):
        return (
            "Doanh nghiệp đang duy trì hiệu quả sinh lời trên "
            "vốn đầu tư ở mức cao trong bối cảnh nhu cầu mở rộng "
            "vốn hiện hữu tương đối hạn chế. NOPAT vẫn được duy "
            "trì trong khi quy mô vốn đầu tư không tiếp tục mở "
            "rộng, cho thấy nền vốn hiện tại đang được khai thác "
            "với hiệu suất tốt. Đặc điểm này phù hợp với một "
            "doanh nghiệp trưởng thành có khả năng tạo lợi nhuận "
            "cao trên nền vốn hiện hữu, dù dư địa tái đầu tư để "
            "tạo tăng trưởng mới cần được đánh giá riêng."
        )

    if (
        efficiency_regime
        == "stable_capital_efficiency"
        and efficiency_profile
        == "stable_capital_productivity"
        and latest_roic is not None
        and latest_roic >= 0.15
    ):
        return (
            "Hiệu quả sử dụng vốn đang duy trì ở mức cao và "
            "tương đối ổn định. Khả năng tạo lợi nhuận trên nền "
            "vốn đầu tư hiện hữu cho thấy doanh nghiệp đang vận "
            "hành với năng suất vốn tích cực, dù chưa có đủ bằng "
            "chứng để xác nhận một chu kỳ tái đầu tư mở rộng mới."
        )

    # ========================================================
    # WEAK EXISTING CAPITAL BASE
    # ========================================================

    if (
        "low_existing_capital_efficiency"
        in efficiency_signals
        or "weak_roic"
        in efficiency_signals
    ):
        return (
            "Hiệu quả sinh lời trên nền vốn hiện hữu vẫn ở mức "
            "thấp. Doanh nghiệp cần cải thiện khả năng tạo lợi "
            "nhuận trên phần vốn đang sử dụng trước khi có thể "
            "xác nhận chất lượng tái đầu tư ở mức tích cực."
        )

    # ========================================================
    # DEFAULT
    # ========================================================

    return (
        "Hiệu quả phân bổ vốn hiện chưa có tín hiệu đủ mạnh để "
        "hình thành một nhận định độc lập về chất lượng tái đầu tư."
    )


# ============================================================
# BUILD KEY WATCH
# ============================================================


def build_key_watch_view(
    warnings,
    financial_cross_signals,
    capital_efficiency_result,
    capital_allocation_result,
):
    warning_set = set(
        warnings
        or []
    )

    cross_signals = set(
        financial_cross_signals
        or []
    )

    efficiency_signals = _get_signals(
        capital_efficiency_result
    )

    allocation_signals = _get_signals(
        capital_allocation_result
    )

    # ========================================================
    # DEBT SERVICE CONTEXT
    # ========================================================

    strong_debt_service_capacity = (
        "strong_debt_service_capacity"
        in cross_signals
    )

    debt_absorption_improving = (
        "debt_absorption_capacity_improving"
        in cross_signals
    )

    debt_service_resilience = (
        "debt_service_resilience_confirmed"
        in cross_signals
    )

    productive_investment_with_debt_capacity = (
        "productive_investment_supported_by_debt_capacity"
        in cross_signals
    )

    external_funding_absorbed = (
        "external_funding_absorbed_by_earnings_growth"
        in cross_signals
    )

    productive_reinvestment_with_debt_service = (
        "productive_reinvestment_with_strong_debt_service"
        in cross_signals
    )

    cashflow_supports_debt_service = (
        "cashflow_supports_debt_service_capacity"
        in cross_signals
    )

    # ========================================================
    # CRITICAL DEBT SERVICE STRESS
    # HIGHEST PRIORITY
    # ========================================================

    if (
        "debt_service_stress_confirmed"
        in cross_signals
        or "critical_debt_service_stress"
        in cross_signals
    ):
        watch = (
            "Năng lực trả lãi đang chịu áp lực nghiêm trọng khi "
            "khả năng bao phủ chi phí lãi vay suy giảm mạnh. "
            "Diễn biến này cho thấy lợi nhuận hoạt động hiện "
            "không còn tạo ra lớp đệm đủ an toàn trước nghĩa vụ "
            "lãi vay."
        )

        if (
            "debt_growth_exceeds_earnings_absorption"
            in cross_signals
        ):
            watch += (
                " Đồng thời, tốc độ mở rộng nợ vay đang vượt "
                "khả năng tăng trưởng lợi nhuận vận hành, cho "
                "thấy năng lực hấp thụ phần nợ tăng thêm đang "
                "suy yếu."
            )

        if (
            "weak_cash_support_for_debt"
            in cross_signals
        ):
            watch += (
                " Mức hỗ trợ của dòng tiền hoạt động đối với "
                "quy mô nợ hiện ở mức thấp, làm giảm khả năng "
                "bù đắp áp lực tài chính bằng nguồn tiền tạo ra "
                "từ hoạt động kinh doanh."
            )

        if (
            "funding_pressure_with_debt_service_stress"
            in cross_signals
            or (
                "investment_pressure_exceeds_debt_absorption"
                in cross_signals
            )
        ):
            watch += (
                " Trong bối cảnh nhu cầu vốn và áp lực tài trợ "
                "vẫn hiện hữu, sự suy yếu của năng lực trả lãi "
                "làm gia tăng rủi ro tài chính và hạn chế dư địa "
                "tiếp tục sử dụng nguồn vốn bên ngoài."
            )

        watch += (
            " Khả năng phục hồi lợi nhuận hoạt động, cải thiện "
            "khả năng bao phủ lãi vay và kiểm soát tốc độ tăng "
            "nợ là các yếu tố trọng yếu cần được theo dõi trong "
            "các kỳ tiếp theo."
        )

        return watch

    # ========================================================
    # PERSISTENT FCF DEFICIT + EXTERNAL FUNDING
    # ========================================================

    if (
        "persistent_fcf_deficit_with_net_debt"
        in cross_signals
        or "persistent_fcf_deficit_with_rising_debt"
        in cross_signals
        or "external_funding_dependence_rising"
        in cross_signals
    ):
        watch = (
            "Dòng tiền tự do âm kéo dài cho thấy nhu cầu đầu tư "
            "thường xuyên vượt khả năng tự tài trợ từ dòng tiền "
            "hoạt động, làm gia tăng mức độ phụ thuộc vào nguồn "
            "vốn bên ngoài."
        )

        if (
            strong_debt_service_capacity
            and debt_absorption_improving
        ):
            watch += (
                " Tuy nhiên, khả năng thanh toán lãi vay hiện "
                "duy trì ở mức cao và năng lực lợi nhuận hoạt "
                "động đang tăng nhanh hơn tốc độ mở rộng nợ vay. "
                "Điều này cho thấy áp lực tài trợ hiện chưa "
                "chuyển hóa thành áp lực trả lãi đáng kể và khả "
                "năng hấp thụ phần nợ tăng thêm đang được cải thiện."
            )

        elif strong_debt_service_capacity:
            watch += (
                " Tuy nhiên, khả năng thanh toán lãi vay hiện "
                "vẫn duy trì ở mức tích cực, tạo lớp đệm nhất "
                "định trước áp lực tài trợ từ chu kỳ đầu tư."
            )

        if (
            productive_investment_with_debt_capacity
            or productive_reinvestment_with_debt_service
            or external_funding_absorbed
        ):
            watch += (
                " Đồng thời, phần vốn đầu tư mới đang tạo ra "
                "mức sinh lời cao hơn nền vốn hiện hữu và tăng "
                "trưởng lợi nhuận vận hành đang hỗ trợ khả năng "
                "hấp thụ nguồn vốn bên ngoài. Diễn biến này phù "
                "hợp với đặc điểm của một chu kỳ tái đầu tư có "
                "tính sản xuất thay vì chỉ phản ánh sự suy yếu "
                "của dòng tiền."
            )

        if (
            "operating_cashflow_momentum_improving"
            in cross_signals
            and "investment_intensity_moderating"
            in cross_signals
        ):
            watch += (
                " Dòng tiền hoạt động đang cải thiện và cường "
                "độ đầu tư có dấu hiệu hạ nhiệt, cho thấy áp lực "
                "tài trợ đầu tư đang có tín hiệu giảm trong kỳ "
                "gần nhất."
            )

        if (
            debt_service_resilience
            and (
                "strong_incremental_returns"
                in allocation_signals
                or (
                    "incremental_capital_materially_more_productive"
                    in efficiency_signals
                )
            )
        ):
            watch += (
                " Khả năng duy trì hiệu quả của phần vốn đầu tư "
                "mới, đồng thời giữ năng lực trả lãi ở mức cao "
                "và từng bước cải thiện mức độ tự tài trợ cho "
                "đầu tư, là yếu tố quan trọng cần được theo dõi "
                "trong các kỳ tiếp theo."
            )

        elif (
            "strong_incremental_returns"
            in allocation_signals
            or (
                "incremental_capital_materially_more_productive"
                in efficiency_signals
            )
        ):
            watch += (
                " Khả năng duy trì hiệu quả của phần vốn đầu tư "
                "mới, đồng thời cải thiện mức độ tự tài trợ cho "
                "đầu tư, là yếu tố quan trọng cần được theo dõi "
                "trong các kỳ tiếp theo."
            )

        else:
            watch += (
                " Khả năng cải thiện mức độ tự tài trợ cho đầu "
                "tư và kiểm soát nhu cầu vốn bên ngoài là yếu tố "
                "quan trọng cần được theo dõi trong các kỳ tiếp theo."
            )

        return watch

    # ========================================================
    # GROSS MARGIN PRESSURE
    # ========================================================

    if (
        "gross_margin_down"
        in warning_set
    ):
        return (
            "Xu hướng thu hẹp biên lợi nhuận gộp là yếu tố "
            "quan trọng cần được theo dõi. Nếu áp lực tại cấp "
            "độ lợi nhuận gộp tiếp tục kéo dài, khả năng duy trì "
            "tốc độ tăng trưởng lợi nhuận có thể suy giảm."
        )

    # ========================================================
    # NEGATIVE FCF
    # ========================================================

    if (
        "negative_fcf_with_rising_debt"
        in warning_set
    ):
        if strong_debt_service_capacity:
            return (
                "Dòng tiền tự do âm đi cùng xu hướng gia tăng "
                "nợ vay cho thấy nhu cầu đầu tư đang tạo áp lực "
                "lên nguồn tài trợ. Tuy nhiên, khả năng thanh "
                "toán lãi vay hiện vẫn duy trì ở mức tích cực. "
                "Khả năng cải thiện dòng tiền tự do và kiểm soát "
                "tốc độ tăng nợ là yếu tố cần được theo dõi."
            )

        return (
            "Dòng tiền tự do âm đi cùng xu hướng gia tăng nợ vay "
            "cho thấy nhu cầu đầu tư đang tạo áp lực lên nguồn "
            "tài trợ. Khả năng cải thiện dòng tiền tự do và kiểm "
            "soát tốc độ tăng nợ là yếu tố cần được theo dõi."
        )

    # ========================================================
    # WEAK GROWTH MOMENTUM WITH STRONG FINANCIAL BASE
    # ========================================================

    if (
        "weak_growth_momentum"
        in warning_set
    ):
        if (
            "cashflow_supports_debt_service_capacity"
            in cross_signals
            or "strong_debt_service_capacity"
            in cross_signals
            or "balance_sheet_buffer_present"
            in cross_signals
        ):
            return (
                "Nền tảng dòng tiền và cấu trúc tài chính hiện "
                "duy trì tương đối vững, nhưng động lực tăng trưởng "
                "đang ở mức hạn chế. Tốc độ mở rộng doanh thu và "
                "lợi nhuận thấp cho thấy thách thức trọng yếu hiện "
                "không nằm ở khả năng tài trợ hay trả lãi, mà ở "
                "khả năng tái tạo động lực tăng trưởng mới. Khả "
                "năng đẩy nhanh tăng trưởng doanh thu, duy trì hiệu "
                "quả sinh lời và chuyển hóa nền tảng tài chính hiện "
                "có thành tăng trưởng lợi nhuận cao hơn là yếu tố "
                "quan trọng cần được theo dõi trong các kỳ tiếp theo."
            )

        return (
            "Động lực tăng trưởng hiện ở mức hạn chế khi tốc độ "
            "mở rộng doanh thu và lợi nhuận còn thấp. Khả năng "
            "tái tạo tăng trưởng và cải thiện tốc độ gia tăng lợi "
            "nhuận là yếu tố trọng yếu cần được theo dõi trong "
            "các kỳ tiếp theo."
        )

    # ========================================================
    # DEBT SERVICE POSITIVE CONTEXT
    # ========================================================

    if (
        strong_debt_service_capacity
        and debt_service_resilience
    ):
        return (
            "Khả năng thanh toán lãi vay hiện duy trì ở mức cao "
            "và có tính ổn định. Cần tiếp tục theo dõi khả năng "
            "duy trì tăng trưởng lợi nhuận vận hành để bảo toàn "
            "năng lực hấp thụ nợ trong các kỳ tiếp theo."
        )

    if cashflow_supports_debt_service:
        return (
            "Dòng tiền hoạt động hiện đang hỗ trợ tích cực cho "
            "năng lực trả nợ. Khả năng duy trì chất lượng dòng "
            "tiền là yếu tố cần tiếp tục được theo dõi."
        )
    
        # ========================================================
    # HIGH LEVERAGE WITH IMPROVING DEBT ABSORPTION
    # ========================================================

    if (
        "high_financial_leverage"
        in warning_set
        or "debt_absorption_capacity_improving"
        in cross_signals
    ):
        if (
            "debt_absorption_capacity_improving"
            in cross_signals
        ):
            return (
                "Đòn bẩy tài chính hiện vẫn ở mức tương đối cao, "
                "làm gia tăng độ nhạy của cấu trúc tài chính trước "
                "biến động lợi nhuận và chi phí vốn. Tuy nhiên, "
                "năng lực lợi nhuận vận hành đang tăng nhanh hơn "
                "tốc độ mở rộng nợ vay và khả năng bao phủ lãi vay "
                "đang phục hồi, cho thấy năng lực hấp thụ nợ có dấu "
                "hiệu cải thiện. Khả năng tiếp tục nâng lớp đệm trả "
                "lãi trong khi kiểm soát mức đòn bẩy là yếu tố quan "
                "trọng cần được theo dõi trong các kỳ tiếp theo."
            )

        return (
            "Mức đòn bẩy tài chính tương đối cao là yếu tố cần "
            "được theo dõi. Khả năng duy trì dòng tiền hoạt động, "
            "kiểm soát tốc độ tăng nợ và bảo toàn năng lực trả lãi "
            "sẽ quyết định mức độ bền vững của cấu trúc tài chính."
        )

    return (
        "Cần theo dõi thêm các kỳ báo cáo tiếp theo để xác định "
        "khả năng duy trì xu hướng tăng trưởng, hiệu quả sử dụng "
        "vốn và chất lượng dòng tiền."
    )


# ============================================================
# BUILD THESIS
# ============================================================


def build_thesis(
    strengths,
    warnings,
    cross_signals,
    growth_quality_evidence,
    earnings_driver_result,
    financial_cross_signals,
    capital_efficiency_result=None,
    capital_allocation_result=None,
):
    growth_driver = build_growth_driver(
        earnings_driver_result
    )

    growth_quality = (
        build_growth_quality_view(
            growth_quality_evidence
        )
    )

    capital_quality = (
        build_capital_quality_view(
            capital_efficiency_result,
            capital_allocation_result,
        )
    )

    key_watch = build_key_watch_view(
        warnings,
        financial_cross_signals,
        capital_efficiency_result,
        capital_allocation_result,
    )

    thesis_parts = [
        growth_driver,
        growth_quality,
    ]

    if capital_quality:
        thesis_parts.append(
            capital_quality
        )

    thesis_parts.append(
        key_watch
    )

    thesis = " ".join(
        thesis_parts
    )

    return {
        "status": "success",
        "growth_driver": growth_driver,
        "growth_quality": growth_quality,
        "capital_quality": capital_quality,
        "key_watch": key_watch,
        "thesis": thesis,
    }