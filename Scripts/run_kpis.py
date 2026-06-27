import sqlite3
import pandas as pd

conn = sqlite3.connect('../data/supply_chain.db')

queries = {
    "KPI 1: Delivery Status Breakdown": '''
        SELECT "Delivery Status", COUNT(*) as order_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
        FROM orders GROUP BY "Delivery Status" ORDER BY order_count DESC
    ''',
    "KPI 2: Late Rate by Shipping Mode": '''
        SELECT "Shipping Mode", COUNT(*) as total_orders,
        ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct
        FROM orders GROUP BY "Shipping Mode" ORDER BY late_rate_pct DESC
    ''',
    "KPI 3: Late Rate by Region": '''
        SELECT "Order Region", COUNT(*) as total_orders,
        ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct
        FROM orders GROUP BY "Order Region" ORDER BY late_rate_pct DESC
    ''',
    "KPI 4: Shipping Delay Gap": '''
        SELECT "Shipping Mode",
        ROUND(AVG("Days for shipment (scheduled)"), 2) as avg_scheduled,
        ROUND(AVG("Days for shipping (real)"), 2) as avg_actual,
        ROUND(AVG("Days for shipping (real)" - "Days for shipment (scheduled)"), 2) as avg_gap
        FROM orders GROUP BY "Shipping Mode" ORDER BY avg_gap DESC
    ''',
    "KPI 5: Profit Ratio by Category (worst 20)": '''
        SELECT "Category Name", COUNT(*) as order_count,
        ROUND(SUM(Sales), 2) as total_sales,
        ROUND(SUM("Order Profit Per Order"), 2) as total_profit,
        ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio
        FROM orders GROUP BY "Category Name" ORDER BY avg_profit_ratio ASC LIMIT 20
    ''',
    "KPI 6: Profit by Customer Segment": '''
        SELECT "Customer Segment", COUNT(*) as order_count,
        ROUND(SUM(Sales), 2) as total_sales,
        ROUND(SUM("Order Profit Per Order"), 2) as total_profit,
        ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio
        FROM orders GROUP BY "Customer Segment" ORDER BY total_profit DESC
    ''',
    "KPI 7: Discount Band vs Profit": '''
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
        FROM orders GROUP BY discount_band ORDER BY avg_profit_ratio DESC
    ''',
    "KPI 8: Monthly Order/Sales Trend": '''
        SELECT strftime('%Y-%m', "order date (DateOrders)") as order_month,
        COUNT(*) as order_count,
        ROUND(SUM(Sales), 2) as total_sales
        FROM orders GROUP BY order_month ORDER BY order_month
    ''',
    "KPI 9: Worst Performing Regions": '''
        SELECT "Order Region", COUNT(*) as total_orders,
        ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct,
        ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio
        FROM orders GROUP BY "Order Region" ORDER BY late_rate_pct DESC LIMIT 5
    ''',
    "KPI 10: Late Rate by Category (top 15 worst)": '''
    SELECT "Category Name", COUNT(*) as total_orders,
    ROUND(SUM(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_rate_pct,
    ROUND(AVG("Order Item Profit Ratio"), 4) as avg_profit_ratio
    FROM orders GROUP BY "Category Name" ORDER BY late_rate_pct DESC LIMIT 15
''',
"DATE CHECK: Min/Max Order Dates": '''
    SELECT 
    MIN("order date (DateOrders)") as earliest_order,
    MAX("order date (DateOrders)") as latest_order,
    COUNT(*) as total_rows
    FROM orders
''',
"DATE CHECK: Daily order count for January 2018": '''
    SELECT 
    DATE("order date (DateOrders)") as order_day,
    COUNT(*) as order_count
    FROM orders
    WHERE strftime('%Y-%m', "order date (DateOrders)") = '2018-01'
    GROUP BY order_day
    ORDER BY order_day
''',
}

for title, query in queries.items():
    print(f"\n=== {title} ===")
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

conn.close()