

SELECT
    t.transaction_id,
    t.date,
    t.user_id,
    t.driver_id,
    t.merchant_id,
    t.service_id,
    t.quantity,
    t.base_amount,
    t.discounted_amount,
    t.total_amount,
    t.payment_method,
    t.department,
    t.city,
    t.region,
    t.promotion_id,
    u.name AS user_name,
    u.loyalty_tier,
    u.churn_risk_score,
    d.name AS driver_name,
    d.vehicle_type AS driver_vehicle_type,
    d.driver_rating,
    m.merchant_name,
    m.service_type AS merchant_service_type
FROM "swifthub"."main"."stg_transactions" t
LEFT JOIN "swifthub"."main"."stg_users" u ON t.user_id = u.user_id
LEFT JOIN "swifthub"."main"."stg_drivers" d ON t.driver_id = d.driver_id
LEFT JOIN "swifthub"."main"."stg_merchants" m ON t.merchant_id = m.merchant_id