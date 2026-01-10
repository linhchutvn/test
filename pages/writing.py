import streamlit as st

st.set_page_config(page_title="Luyện tập", layout="wide", page_icon="📝")

# --- CSS ĐỂ ẨN SIDEBAR MẶC ĐỊNH VÀ TRANG TRÍ MENU ---
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;} /* Ẩn sidebar trái */
    
    /* Trang trí nút Menu */
    .stButton a {
        text-decoration: none;
    }
    hr {margin-top: 0.5rem; margin-bottom: 1rem;}
</style>
""", unsafe_allow_html=True)

# --- THANH MENU ĐIỀU HƯỚNG (NAVBAR) ---
# Tạo 2 cột cho 2 nút menu
col1, col2, col3 = st.columns([1, 1, 4]) # col3 là khoảng trống

with col1:
    # Nút dẫn về trang chủ (app.py)
    st.page_link("app.py", label="🏠 My Homepage", icon=None, use_container_width=True)

with col2:
    # Nút dẫn đến trang hiện tại (làm mờ hoặc đổi màu nếu muốn)
    st.page_link("pages/luyentap.py", label="📝 Luyện tập 4 kỹ năng", icon=None, use_container_width=True)

st.divider() # Đường kẻ ngang phân cách menu

# --- NỘI DUNG CHÍNH CỦA TRANG LUYỆN TẬP (YOUPASS) ---
st.markdown("""
<style>
    .exam-card { background-color: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 20px; display: flex; gap: 15px; }
    .exam-tag { background-color: #1e272e; color: white; padding: 3px 8px; font-size: 10px; border-radius: 4px; position: absolute; }
    .exam-thumb { width: 120px; height: 80px; object-fit: cover; border-radius: 6px; }
    .exam-title { color: #0984e3; font-weight: bold; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

col_menu, col_content = st.columns([1, 4])
with col_menu:
    st.markdown("### YouPass Collect")
    st.info("💡 Review đề thi thật")
    mode = st.radio("Chọn kỹ năng", ["Reading", "Listening", "Writing"])

with col_content:
    st.markdown(f"#### 🕒 Danh sách bài tập: {mode}")
    exercises = [
        {"type": "Table", "title": "The table below illustrates weekly consumption...", "img": "https://via.placeholder.com/150x100?text=Table"},
        {"type": "Map", "title": "Coal mining site redevelopment...", "img": "https://via.placeholder.com/150x100?text=Map"},
    ]
    grid = st.columns(2)
    for i, ex in enumerate(exercises):
        with grid[i % 2]:
            st.markdown(f"""
            <div class="exam-card">
                <span class="exam-tag">{ex['type']}</span>
                <img src="{ex['img']}" class="exam-thumb">
                <div><a href="#" class="exam-title">{ex['title']}</a></div>
            </div>
            """, unsafe_allow_html=True)
