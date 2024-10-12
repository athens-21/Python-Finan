import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#รับข้อมูลพื้นฐานของบริษัทจากผู้ใช้
def get_financial_data():
    def get_input(prompt):
        return float(input(prompt).replace(',', ''))

    net_income = get_input("Enter net income (กำไรสุทธิ ล้านบาท): ")  # กำไรสุทธิ
    current_price = get_input("Enter current stock price (ราคาหุ้นปัจจุบัน): ")  # ราคาหุ้นปัจจุบัน
    risk_free_rate = get_input("Enter risk-free rate (RFR in %): ")  # อัตราผลตอบแทนปราศจากความเสี่ยง
    market_return = get_input("Enter expected market return (Rm in %): ")  # อัตราผลตอบแทนตลาด
    beta = get_input("Enter Beta: ")  # ค่า Beta ของหุ้น
    dividend_yield = get_input("Enter Dividend Yield (%): ")  # Dividend Yield
    historical_prices = input("Enter historical prices (comma-separated): ")  # ราคาหุ้นในอดีต
    historical_prices = list(map(float, historical_prices.split(',')))  # แปลงราคาหุ้นในอดีตเป็น list
    intrinsic_price = get_input("Enter intrinsic price (มูลค่าที่แท้จริง): ")  # รับมูลค่าที่แท้จริง
    average_price = get_input("Enter average price (ราคาเฉลี่ย): ")  # รับราคาที่เฉลี่ย

    data = {
        'net_income': net_income,
        'current_price': current_price,
        'risk_free_rate': risk_free_rate / 100,  # แปลงเป็นค่าเปอร์เซ็นต์
        'market_return': market_return / 100,  # แปลงเป็นค่าเปอร์เซ็นต์
        'beta': beta,
        'dividend_yield': dividend_yield / 100,  # แปลงเป็นค่าเปอร์เซ็นต์
        'historical_prices': historical_prices,
        'intrinsic_price': intrinsic_price,  # เพิ่มมูลค่าที่แท้จริงใน dict
        'average_price': average_price  # เพิ่มราคาเฉลี่ยใน dict
    }

    return pd.DataFrame([data])

# คำนวณมูลค่าที่แท้จริงด้วย DCF
def discounted_cash_flow(net_income, growth_rate, discount_rate, years):
    cash_flows = [net_income * (1 + growth_rate) ** year for year in range(1, years + 1)]
    dcf_value = sum([cf / (1 + discount_rate) ** year for year, cf in enumerate(cash_flows, 1)])
    return dcf_value

# คำนวณ CAPM
def calculate_capm(risk_free_rate, market_return, beta):
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return expected_return

# ประเมินมูลค่าหุ้นและตัดสินใจซื้อหรือขาย
def investment_decision(intrinsic_value, current_price):
    if intrinsic_value > current_price:
        return "Buy"
    elif intrinsic_value < current_price:
        return "Sell"
    else:
        return "Hold"

#วิเคราะห์ผลลัพธ์
def analyze_investment(average_price, intrinsic_price, dividend_yield):
    R = ((average_price - intrinsic_price) / intrinsic_price) + dividend_yield
    return R

financial_data = get_financial_data()  # รับข้อมูลจากผู้ใช้

# คำนวณมูลค่าที่แท้จริงด้วย DCF
net_income = financial_data['net_income'].values[0]
intrinsic_value = discounted_cash_flow(net_income, growth_rate=0.05, discount_rate=0.08, years=5)

# ราคาหุ้นปัจจุบัน
current_price = financial_data['current_price'].values[0]

# คำนวณ CAPM
risk_free_rate = financial_data['risk_free_rate'].values[0]
market_return = financial_data['market_return'].values[0]
beta = financial_data['beta'].values[0]

expected_return = calculate_capm(risk_free_rate, market_return, beta)

# ตัดสินใจลงทุน
decision = investment_decision(intrinsic_value, current_price)

# ดึงมูลค่าที่แท้จริงที่ผู้ใช้ป้อน
intrinsic_price = financial_data['intrinsic_price'].values[0]
dividend_yield = financial_data['dividend_yield'].values[0]
average_price = financial_data['average_price'].values[0]

# วิเคราะห์การลงทุน
R = analyze_investment(average_price, intrinsic_price, dividend_yield)

# วิเคราะห์ผลลัพธ์
if R > expected_return:
    investment_decision_result = "ควรลงทุน"
else:
    investment_decision_result = "ไม่ควรลงทุน"

# แสดงผลการคำนวณ
print(f"Current Price: {current_price:.2f} Baht")
print(f"Investment Decision: {decision}")
print(f"Expected Return (CAPM): {expected_return * 100:.2f}%")
print(f"ราคาเฉลี่ย: {average_price:.2f} Baht")
print(f"Div%: {dividend_yield * 100:.2f}%")
print(f"R: {R:.4f}")
print(f"การตัดสินใจลงทุน: {investment_decision_result}")
