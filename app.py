import streamlit as st
import pandas as pd
import os
import datetime

# 定義記帳檔案名稱
FILE_NAME = "expense_record.csv"

# 初始化檔案：如果檔案不存在，就建立一個有標頭的 CSV
if not os.path.exists(FILE_NAME):
    df_init = pd.DataFrame(columns=["日期", "類別", "金額", "備註"])
    df_init.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')

# 網頁標題與介紹
st.set_page_config(page_title="個人記帳與消費分析工具", layout="centered")
st.title("💰 個人記帳與消費分析網頁系統")

st.markdown("---")

# ================= 介面佈局：左側邊欄輸入，右側主畫面顯示 =================

# 左側：新增記帳表單
st.sidebar.header("📝 新增消費紀錄")
with st.sidebar.form(key="expense_form", clear_on_submit=True):
    date = st.date_input("選擇日期", datetime.date.today())
    category = st.selectbox("消費類別", ["餐飲", "交通", "娛樂", "學習", "其他"])
    amount = st.number_input("輸入金額", min_value=0.0, step=10.0)
    description = st.text_input("備註（例如：買晚餐）")
    
    submit_button = st.form_submit_button(label="儲存紀錄")

# 當按下儲存按鈕時的處理邏輯
if submit_button:
    if amount == 0:
        st.sidebar.error("❌ 金額不能為 0 元！")
    else:
        # 讀取現有資料並加入新資料
        new_data = pd.DataFrame([[date, category, amount, description]], columns=["日期", "類別", "金額", "備註"])
        new_data.to_csv(FILE_NAME, mode='a', header=False, index=False, encoding='utf-8-sig')
        st.sidebar.success(f"✅ 成功記錄：{category} 支出 {amount} 元！")

# ================= 右側主畫面：歷史紀錄與統計分析 =================

# 讀取最新的 CSV 資料
df = pd.read_csv(FILE_NAME, encoding='utf-8-sig')

# 檢查是否有資料
if df.empty:
    st.info("💡 目前還沒有任何記帳紀錄，請從左側邊欄開始新增第一筆吧！")
else:
    # 區塊一：關鍵指標數據 (Metrics)
    total_spend = df["金額"].sum()
    st.subheader("財務總覽")
    
    col1, col2 = st.columns(2)
    col1.metric(label="目前總消費金額", value=f"${total_spend:,.0f} 元")
    col2.metric(label="總記帳筆數", value=f"{len(df)} 筆")
    
    st.markdown("---")
    
    # 區塊二：消費分析圖表
    st.subheader("消費結構圖表分析")
    
    # 按類別將金額加總
    category_totals = df.groupby("類別")["金額"].sum().reset_index()
    
    # 利用 Streamlit 內建的圖表工具，一鍵生成漂亮的長條圖
    st.bar_chart(data=category_totals, x="類別", y="金額", use_container_width=True)
    
    st.markdown("---")
    
    # 區塊三：詳細歷史明細表格
    st.subheader("歷史記帳明細")
    # 將日期排序，讓最新的記帳呈現在最上面
    df_sorted = df.sort_values(by="日期", ascending=False)
    df_sorted.index = range(1, len(df_sorted) + 1)
    
    st.dataframe(df_sorted, use_container_width=True)
    
    # 清空歷史紀錄按鈕（方便測試或重新展示）
    if st.button("清空所有歷史紀錄"):
        df_empty = pd.DataFrame(columns=["日期", "類別", "金額", "備註"])
        df_empty.to_csv(FILE_NAME, index=False, encoding='utf-8-sig') # 這裡修正為 to_csv 了！
        st.rerun()