import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import json
import re

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="IELTS Task 1 Intelligent Tutor", layout="wide")

# CSS để giao diện giống mẫu (Khung xám, ô nhập liệu)
st.markdown("""
<style>
    .guide-box {
        background-color: #f8f9fa;
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: #31333F;
    }
    .guide-title {
        font-weight: bold;
        margin-bottom: 5px;
        color: #ff4b4b;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC KẾT NỐI AI (CỦA BẠN) ---
# Lấy Key từ secrets
try:
    ALL_KEYS = st.secrets["GEMINI_API_KEYS"]
except Exception:
    st.error("Chưa cấu hình secrets.toml hoặc thiếu GEMINI_API_KEYS")
    st.stop()

def generate_content_with_failover(prompt, image=None):
    """Hàm thông minh tự động dò tìm Model tốt nhất có sẵn lượt dùng"""
    keys_to_try = list(ALL_KEYS)
    random.shuffle(keys_to_try) 
    
    # DANH SÁCH ƯU TIÊN
    model_priority = [
        "gemini-2.0-flash-thinking-preview-01-21",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro", 
        "gemini-1.5-flash"
    ]
    
    last_error = ""
    for index, current_key in enumerate(keys_to_try): 
        try:
            genai.configure(api_key=current_key)
            
            # Lấy danh sách model
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Tìm model tốt nhất
            sel_model = None
            for target in model_priority:
                if any(target in m_name for m_name in available_models):
                    sel_model = target
                    break
            
            if not sel_model:
                sel_model = "gemini-1.5-flash" 

            # Hiển thị kết nối (Debug)
            masked_key = f"****{current_key[-4:]}"
            with st.expander("🔌 Trạng thái kết nối AI", expanded=False):
                st.write(f"**Model:** `{sel_model}`")
                st.write(f"**Key:** `{masked_key}` (Key #{index + 1})")

            # Khởi tạo model
            temp_model = genai.GenerativeModel(model_name=sel_model)
            
            content_parts = [prompt]
            if image:
                content_parts.append(image)
                
            gen_config = {
                "temperature": 0.4,       
                "top_p": 0.95,           
                "top_k": 64,             
                "max_output_tokens": 8192,
                "response_mime_type": "application/json" # Ép kiểu trả về JSON để dễ xử lý
            }

            # Config cho Thinking model (nếu có)
            if "thinking" in sel_model.lower():
                # Thinking model hiện chưa hỗ trợ ép kiểu JSON qua MIME type chặt chẽ ở một số version,
                # nên ta bỏ mime_type nếu là thinking để tránh lỗi, và xử lý chuỗi sau.
                del gen_config["response_mime_type"]
                gen_config["thinking_config"] = {"include_thoughts": False, "thinking_budget": 1024}

            response = temp_model.generate_content(
                content_parts,
                generation_config=gen_config
            )
            
            return response, sel_model 
            
        except Exception as e:
            last_error = str(e)
            if "429" in last_error or "quota" in last_error.lower():
                continue 
            else:
                # Lỗi khác (400, 500) thì break luôn
                break
                
    st.error(f"❌ Kết nối thất bại. Lỗi: {last_error}")
    return None, None

# --- XỬ LÝ KẾT QUẢ TỪ AI ---
def parse_ai_response(response_text):
    """Làm sạch và chuyển đổi text AI trả về thành Dictionary"""
    try:
        # Xóa các ký tự markdown json nếu có
        clean_text = re.sub(r'```json\n|```', '', response_text).strip()
        data = json.loads(clean_text)
        return data
    except json.JSONDecodeError:
        st.error("AI trả về định dạng dữ liệu không đúng. Vui lòng thử lại.")
        return None

# --- GIAO DIỆN CHÍNH ---

st.title("✍️ IELTS Writing Task 1 Simulator")
st.caption("Nhập đề bài, tải ảnh và nhận hướng dẫn chi tiết từ AI để thực hành.")

col_input, col_img = st.columns([1, 1])

with col_input:
    st.subheader("1. Đề bài")
    question_text = st.text_area("Nhập câu hỏi (Question Prompt):", height=200, placeholder="The chart below shows...")

with col_img:
    st.subheader("2. Hình ảnh")
    uploaded_file = st.file_uploader("Upload ảnh biểu đồ/bản đồ", type=['png', 'jpg', 'jpeg'])
    img_data = None
    if uploaded_file:
        img_data = Image.open(uploaded_file)
        st.image(img_data, caption="Đề bài", use_container_width=True)

# Khởi tạo session state
if "guide_data" not in st.session_state:
    st.session_state.guide_data = None

# Nút Action
if st.button("🚀 Hướng Dẫn & Lập Dàn Ý", type="primary"):
    if not question_text and not img_data:
        st.warning("Vui lòng nhập ít nhất câu hỏi hoặc hình ảnh.")
    else:
        with st.spinner("AI đang phân tích biểu đồ và lập hướng dẫn..."):
            # Prompt Engineering: Ép AI trả về JSON cấu trúc chuẩn
            system_prompt = """
            Bạn là một chuyên gia IELTS Writing Task 1. Hãy phân tích đề bài và hình ảnh được cung cấp.
            Nhiệm vụ:
            1. Xác định loại biểu đồ (Line, Bar, Map, Process, Mixed, etc.).
            2. Viết hướng dẫn chi tiết bằng TIẾNG VIỆT cho 4 phần: Introduction, Overview, Body 1, Body 2.
            
            Yêu cầu format OUTPUT là JSON với các key sau:
            {
                "task_type": "Loại biểu đồ (Ví dụ: Process Diagram)",
                "introduction_guide": "Hướng dẫn cách paraphrase đề bài...",
                "overview_guide": "Hướng dẫn viết câu nhận xét chung (xu hướng/đặc điểm nổi bật)...",
                "body1_guide": "Hướng dẫn chi tiết nhóm thông tin 1...",
                "body2_guide": "Hướng dẫn chi tiết nhóm thông tin 2..."
            }
            Chỉ trả về JSON, không thêm lời dẫn.
            """
            
            # Gọi hàm AI của bạn
            response, model_used = generate_content_with_failover(system_prompt + "\n\nĐề bài: " + question_text, img_data)
            
            if response:
                result_json = parse_ai_response(response.text)
                if result_json:
                    st.session_state.guide_data = result_json
                    st.toast("Đã phân tích xong!", icon="✅")

# --- KHU VỰC THỰC HÀNH ---

if st.session_state.guide_data:
    data = st.session_state.guide_data
    
    st.markdown("---")
    st.info(f"📌 **Loại bài:** {data.get('task_type', 'Task 1')}")

    # Hàm render từng section
    def render_section(title, guide_content, key_name):
        st.markdown(f"### {title}")
        
        # Phần hướng dẫn từ AI (màu xám)
        st.markdown(f"""
        <div class="guide-box">
            <div class="guide-title">💡 Hướng dẫn {title}:</div>
            {guide_content}
        </div>
        """, unsafe_allow_html=True)
        
        # Ô nhập liệu
        user_input = st.text_area(f"Viết phần {title} của bạn:", height=150, key=key_name)
        
        # Word count
        words = len(user_input.split()) if user_input else 0
        st.caption(f"Số từ: {words}")
        return user_input

    # 1. Introduction
    intro = render_section("Introduction", data.get("introduction_guide", ""), "input_intro")
    
    # 2. Overview
    overview = render_section("Overview", data.get("overview_guide", ""), "input_overview")
    
    # 3. Body 1
    body1 = render_section("Body 1", data.get("body1_guide", ""), "input_body1")
    
    # 4. Body 2
    body2 = render_section("Body 2", data.get("body2_guide", ""), "input_body2")

    # Tổng kết
    st.markdown("---")
    total_words = len(intro.split()) + len(overview.split()) + len(body1.split()) + len(body2.split())
    st.metric(label="Tổng số từ bài viết", value=total_words)
    
    full_essay = f"{intro}\n\n{overview}\n\n{body1}\n\n{body2}"
    if st.button("📋 Copy toàn bộ bài viết"):
        st.code(full_essay, language='text')
