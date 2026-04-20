# Market Dynamics: Indonesian Seasonal Forecasting

This project analyzes transactional history to identify and project future growth patterns tailored to the Indonesian market.

## Implementation Overview
The forecasting models aggregate transactional data from the `fact_daily_revenue` marts to identify local seasonality.

### Key Seasonal Drivers:
- **Ramadan & Lebaran**: Significant peaks in food delivery (Foodora) and logistics (ParcelPro) due to gifting and religious observance.
- **Payday Halos**: Consistent spend spikes occurring between the 25th and 5th of each month.
- **Double Date Sales**: "Twin dates" (e.g., 10.10, 11.11, 12.12 Harbolnas) which drive massive e-commerce and digital payment volume.

## Forecast Interpretation
- **Trend Line**: Represents the organic growth of the SwiftHub user base.
- **Seasonality Plot**: Visualizes the recurring weekly and monthly rhythms of the Indonesian digital economy.
- **Anomaly Detection**: Flags sudden deviations from the forecast, which often correlate with localized service outages or highly successful ad-hoc promotions.
