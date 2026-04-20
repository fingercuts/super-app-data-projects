# Reporting Reference: Business Metrics & Insights

This guide defines the key performance indicators (KPIs) and analytical frameworks supported by the SwiftHub Data Warehouse.

## 1. Financial Performance
- **Gross Revenue (`total_amount`)**: Total raw value of transactions before any discounts.
- **Average Order Value (AOV)**: Calculated as `SUM(total_amount) / COUNT(*)`.
- **Department Contribution**: Revenue breakdown by Super App verticals (RideWay, Foodora, etc.).

## 2. Growth & Engagement
- **Active Users**: Count of unique `user_id` with at least one transaction in the current window.
- **Transaction Velocity**: Frequency of orders per user/driver over time.
- **Regional Hotspots**: Transaction density mapped across Indonesian hubs (Jakarta, Surabaya, Bali).

## 3. Operations & Logistics
- **Fleet Efficiency**: Ratio of active drivers to completed orders.
- **Service Utilization**: Adoption rates of specific on-demand services (e.g., RideWay Go vs. Car).

## 4. Promotion Impact
- **Marketing Lift**: Increase in transactional volume during localized Indonesian holidays (Lebaran, Harbolnas).
- **Discount Efficiency**: Impact of `discounted_amount` on total volume growth.
