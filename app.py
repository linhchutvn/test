import streamlit as st

# 1. Cấu hình trang
st.set_page_config(page_title="AuViet Center", layout="wide", page_icon="🎓")

# ----------------------------------------------------------------
# PHẦN CSS (GIAO DIỆN)
# ----------------------------------------------------------------
st.markdown("""
<style>
    /* 1. CSS CHO THẺ SẢN PHẨM (CARD) - Giữ nguyên như cũ */
    .product-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: 0.3s;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .product-card:hover {
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transform: translateY(-5px);
    }
    .card-img {
        width: 100%;
        border-radius: 5px;
        object-fit: cover;
        height: 180px; 
        margin-bottom: 10px;
    }
    .course-title {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 5px !important;
        line-height: 1.3;
        min-height: 50px;
    }
    .course-cat { font-size: 13px; color: #7f8c8d; margin-bottom: 5px !important; }
    .course-price { color: #d63031; font-weight: bold; font-size: 16px; margin-bottom: 15px !important; }
    
    /* Nút xem chi tiết */
    .custom-btn {
        display: inline-block;
        background-color: #00b894; 
        color: white !important;
        padding: 8px 20px;
        border-radius: 20px;
        text-decoration: none !important;
        font-weight: 500;
        font-size: 14px;
        border: none;
    }
    .custom-btn:hover { background-color: #019376; }

    /* 2. CSS CHO NÚT LOGIN GOOGLE */
    .google-btn {
        border: 1px solid #dadce0;
        background-color: white;
        color: #3c4043;
        padding: 8px 15px;
        border-radius: 4px;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        float: right; /* Đẩy sang phải */
    }
    .google-btn:hover { background-color: #f7fafe; border-color: #d2e3fc; }

    /* 3. CSS CHO FOOTER (CHÂN TRANG) */
    .footer-container {
        background-color: white;
        border-top: 1px solid #e0e0e0;
        padding: 40px 0;
        margin-top: 50px;
        color: #333;
    }
    .footer-content {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .footer-left {
        flex: 1;
        min-width: 300px;
        margin-bottom: 20px;
    }
    .footer-right {
        flex: 2;
        min-width: 300px;
    }
    .footer-row {
        display: flex;
        align-items: flex-start; /* Căn lề trên */
        margin-bottom: 15px;
    }
    .footer-icon {
        width: 20px;
        margin-right: 15px;
        font-size: 18px;
    }
    .footer-text {
        font-size: 14px;
        line-height: 1.6;
    }
    .dmca-badge {
        margin-top: 15px;
        width: 120px;
    }
    .copyright {
        text-align: center;
        font-size: 13px;
        color: #666;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)
courses = [
    {"id": 1, "title": "Khoá học IELTS Speaking", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/SPEAKING.png?raw=true", "category": "Speaking", "link": "https://www.youtube.com/playlist?list=PLI3S3xWA78UXXz0m6QoGyc-8UvHeAYTYT"},
    {"id": 2, "title": "Khoá học IELTS Reading", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/READING.png?raw=true", "category": "Reading", "link": "https://www.google.com"},
    {"id": 3, "title": "Khoá học IELTS Listening", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/LISTENING.png?raw=true", "category": "Listening", "link": "https://www.google.com"},
    {"id": 4, "title": "Khoá học IELTS Writing Task 1", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/TASK%201.png?raw=true", "category": "Writing Task 1", "link": "https://www.youtube.com/playlist?list=PLI3S3xWA78UWtIxIEnZia2siEgxJPwpfQ"},
    {"id": 5, "title": "Khoá học IELTS Writing Task 2", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/task%202.png?raw=true", "category": "Writing Task 2", "link": "https://www.youtube.com/playlist?list=PLI3S3xWA78UWM9nT6jYY9vl3mHb52ZQ08"},
    {"id": 6, "title": "Chấm điểm IELTS Writing Task 1", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/Assessment_TASK1.png?raw=true", "category": "Writing Task 1", "link": "https://ielts-albertnguyen.streamlit.app/"},
    {"id": 7, "title": "Chấm điểm IELTS Writing Task 2", "price": "FREE", "img": "https://github.com/linhchutvn/test/blob/main/Assessment_TASK2.png?raw=true", "category": "Writing Task 2", "link": "https://www.google.com"},
]

top_col1, top_col2 = st.columns([8, 2])

with top_col1:
    st.markdown("### 🎓 AuViet Center") # Tên web nhỏ ở góc trái

with top_col2:
    # Nút Login giả lập (Chỉ là giao diện, chưa có chức năng thật)
    st.markdown("""
        <a href="https://accounts.google.com" target="_blank" class="google-btn">
            <img src="https://www.svgrepo.com/show/475656/google-color.svg" width="20" height="20">
            Đăng nhập Google
        </a>
    """, unsafe_allow_html=True)

st.divider() # Đường kẻ ngang phân cách

# ----------------------------------------------------------------
# THANH TÌM KIẾM & BỘ LỌC NGANG (Thay thế Sidebar)
# ----------------------------------------------------------------
# Chia làm 2 cột: Tìm kiếm (Rộng) - Danh mục (Hẹp)
search_col, filter_col = st.columns([3, 1])

with search_col:
    search_term = st.text_input("🔍 Tìm kiếm khóa học", placeholder="Nhập tên khóa học bạn quan tâm...")

with filter_col:
    categories = ["Tất cả"] + list(set([c['category'] for c in courses]))
    selected_category = st.selectbox("📂 Danh mục", categories)

# ----------------------------------------------------------------
# BANNER
# ----------------------------------------------------------------
try:
    st.image("banner.JPG", use_column_width=True)
except:
    pass 

st.markdown("### 🔥 Các khóa học nổi bật")

# ----------------------------------------------------------------
# LOGIC & HIỂN THỊ KHÓA HỌC
# ----------------------------------------------------------------
filtered_courses = courses
if selected_category != "Tất cả":
    filtered_courses = [c for c in courses if c['category'] == selected_category]
if search_term:
    filtered_courses = [c for c in filtered_courses if search_term.lower() in c['title'].lower()]

if not filtered_courses:
    st.warning("Không tìm thấy khóa học nào!")
else:
    cols = st.columns(3)
    for i, course in enumerate(filtered_courses):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{course['img']}" class="card-img" onerror="this.onerror=null; this.src='https://via.placeholder.com/400x200'">
                <div style="flex-grow: 1;">
                    <p class="course-title">{course['title']}</p>
                    <p class="course-cat">{course['category']}</p>
                    <p class="course-price">{course['price']}</p>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <a href="{course.get('link', '#')}" target="_blank" class="custom-btn">
                        Xem chi tiết
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------------
# FOOTER (CHÂN TRANG) - GIỐNG YOUPASS
# ----------------------------------------------------------------
# Bạn hãy thay link logo.png bằng link ảnh logo thật của bạn
logo_url = "https://raw.githubusercontent.com/username/repo/main/logo.png" 
dmca_url = "https://images.dmca.com/Badges/dmca_protected_sml_120n.png?ID=YOUR_ID" # Ảnh mẫu DMCA

st.markdown(f"""
<div class="footer-container">
    <div class="footer-content">
        <!-- CỘT TRÁI: LOGO & DMCA -->
        <div class="footer-left">
            <!-- Thay src="logo.png" bằng link logo của bạn -->
            <img src="logo.png" style="width: 150px; margin-bottom: 20px;" onerror="this.style.display='none'"> 
            <h4 style="color: #d63031; margin-top: 0;">Âu Việt Center</h4>
            <p style="font-size: 14px; color: #666;">Hệ thống đào tạo IELTS chuyên nghiệp.</p>
            <img src="{dmca_url}" class="dmca-badge">
        </div>

        <!-- CỘT PHẢI: THÔNG TIN LIÊN HỆ -->
        <div class="footer-right">
            <div class="footer-row">
                <span class="footer-icon">📍</span>
                <span class="footer-text">Địa chỉ: 213/9 Nguyễn Gia Trí, Phường Thạnh Mỹ Tây, TP Hồ Chí Minh</span>
            </div>
            <div class="footer-row">
                <span class="footer-icon">💬</span>
                <span class="footer-text">Zalo OA: <a href="https://zalo.me/yourid" target="_blank">https://zalo.me/auviet</a></span>
            </div>
            <div class="footer-row">
                <span class="footer-icon">📞</span>
                <span class="footer-text">Hotline: <b>0866.771.333</b></span>
            </div>
            <div class="footer-row">
                <span class="footer-icon">🔴</span>
                <span class="footer-text">Youtube: <a href="#" target="_blank">https://www.youtube.com/@auviet</a></span>
            </div>
            <div class="footer-row">
                <span class="footer-icon">🎵</span>
                <span class="footer-text">Tiktok: <a href="#" target="_blank">https://www.tiktok.com/@auviet</a></span>
            </div>
        </div>
    </div>
    
    <div class="copyright">
        © 2025 Âu Việt Center. All rights reserved. Developed by Albert Nguyen
    </div>
</div>
""", unsafe_allow_html=True)










