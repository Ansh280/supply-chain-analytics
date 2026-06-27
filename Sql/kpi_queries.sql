-- KPI 1: Overall delivery status breakdown
SELECT 
  "Delivery Status",
  COUNT(*) as order_count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
FROM orders
GROUP BY "Delivery Status"
ORDER BY order_count DESC;

-- KPI 2: Late delivery rate by shipping mode
SELECT 
  "Shipping Mode",
  COUNT(*) as total_orders,
  SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) as late_orders,
  ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct
FROM orders
GROUP BY "Shipping Mode"
ORDER BY late_rate_pct DESC;

-- KPI 3: Late delivery rate by region
SELECT 
  "Order Region",
  COUNT(*) as total_orders,
  ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct
FROM orders
GROUP BY "Order Region"
ORDER BY late_rate_pct DESC;

-- KPI 4: Average actual vs scheduled shipping days (the delay gap)
SELECT 
  "Shipping Mode",
  ROUND(AVG("Days for shipment (scheduled)"), 2) as avg_scheduled_days,
  ROUND(AVG("Days for shipping (real)"), 2) as avg_actual_days,
  ROUND(AVG("Days for shipping (real)" - "Days for shipment (scheduled)"), 2) as avg_delay_gap
FROM orders
GROUP BY "Shipping Mode"
ORDER BY avg_delay_gap DESC;

-- KPI 5: Profit ratio by product category (worst 20 first)
SELECT 
  "Category Name",
  COUNT(*) as order_count,
  ROUND(SUM(Sales), 2) as total_sales,
  ROUND(SUM("Order Profit Per Order"), 2) as total_profit,
  ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio
FROM orders
GROUP BY "Category Name"
ORDER BY avg_profit_ratio ASC
LIMIT 20;

-- KPI 6: Profit by customer segment
SELECT 
  "Customer Segment",
  COUNT(*) as order_count,
  ROUND(SUM(Sales), 2) as total_sales,
  ROUND(SUM("Order Profit Per Order"), 2) as total_profit,
  ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio
FROM orders
GROUP BY "Customer Segment"
ORDER BY total_profit DESC;

-- KPI 7: Discount rate vs profit impact
SELECT 
  CASE 
    WHEN "Order Item Discount Rate" = 0 THEN 'No Discount'
    WHEN "Order Item Discount Rate" <= 0.1 THEN 'Low (0-10%)'
    WHEN "Order Item Discount Rate" <= 0.2 THEN 'Medium (10-20%)'
    ELSE 'High (20%+)'
  END as discount_band,
  COUNT(*) as order_count,
  ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio,
  ROUND(SUM("Order Profit Per Order"), 2) as total_profit
FROM orders
GROUP BY discount_band
ORDER BY avg_profit_ratio DESC;

-- KPI 8: Order volume and sales trend by month
SELECT 
  strftime('%Y-%m', "order date (DateOrders)") as order_month,
  COUNT(*) as order_count,
  ROUND(SUM(Sales), 2) as total_sales
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- KPI 9: Top 5 worst-performing regions (late delivery + low profit combined)
SELECT 
  "Order Region",
  COUNT(*) as total_orders,
  ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct,
  ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio,
  ROUND(SUM("Order Profit Per Order"), 2) as total_profit
FROM orders
GROUP BY "Order Region"
ORDER BY late_rate_pct DESC, avg_profit_ratio ASC
LIMIT 5;