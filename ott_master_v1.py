import streamlit as st
import requests
import os

# [중요] 여기에 본인의 TMDB API Key를 입력하세요!
TMDB_API_KEY = "여기에_본인의_TMDB_API_키를_입력하세요"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# 배경 이미지 경로 (방금 생성된 고퀄리티 이미지)
HERO_IMAGE_PATH = "/Users/bluediamond/.gemini/antigravity/brain/a73afba2-c9e3-4a68-8960-0e9332c2d0b1/ott_master_hero_poster_1775050936800.png"

# 1. 화면 스타일링 (MZ 트렌드: Obsidian Glass)
st.set_page_config(page_title="OTT Master - Prime Edition", page_icon="🎬", layout="wide")

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 기본 배경 */
    .stApp {{ background-color: #0e0e11; color: #f0edf1; font-family: 'Pretendard', sans-serif; }}
    
    /* 히어로 섹션 */
    .hero-container {{
        position: relative;
        height: 450px;
        border-radius: 30px;
        overflow: hidden;
        margin-bottom: 50px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }}
    
    /* 검색바 (히어로 위에 플로팅) */
    .stTextInput > div > div > input {{
        background: rgba(25, 25, 30, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        color: white !important;
        border-radius: 50px !important;
        border: 1px solid rgba(223, 142, 255, 0.3) !important;
        padding: 20px 30px !important;
        font-size: 1.2rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }}

    /* 콘텐츠 카드 디자인 (고급 유리알 버전) */
    .content-card {{
        background: rgba(45, 45, 50, 0.4);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 0px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: left;
        transition: 0.4s ease;
        margin-bottom: 20px;
        overflow: hidden;
    }}
    .content-card:hover {{ 
        transform: translateY(-12px) scale(1.02); 
        border-color: #df8eff;
        box-shadow: 0 15px 40px rgba(223, 142, 255, 0.15);
    }}
    
    .card-info {{ padding: 15px; }}

    /* 태그 스타일 */
    .tag {{
        background: rgba(223, 142, 255, 0.2); color: #df8eff; padding: 4px 10px;
        border-radius: 8px; font-size: 0.75rem; font-weight: 700; margin-right: 5px;
        border: 1px solid rgba(223, 142, 255, 0.4);
    }}
    
    /* 섹션 제목 */
    .section-title {{
        font-size: 1.8rem; font-weight: 800; margin-bottom: 25px; 
        background: linear-gradient(90deg, #f0edf1, #df8eff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
</style>
""", unsafe_allow_html=True)

# API 도움 함수
def fetch_data(endpoint, params={{}}):
    if TMDB_API_KEY == "여기에_본인의_TMDB_API_키를_입력하세요":
        return None
    base_params = {"api_key": TMDB_API_KEY, "language": "ko-KR"}
    base_params.update(params)
    try:
        res = requests.get(f"{TMDB_BASE_URL}{{endpoint}}", params=base_params)
        return res.json()
    except:
        return None

# -------------------------------------------------------------------------
# 상단 메뉴 & 검색창
# -------------------------------------------------------------------------
st.markdown("<h2 style='color: #df8eff; margin-bottom: 5px;'>🎬 OTT MASTER</h2>", unsafe_allow_html=True)

# 검색 입력 (히어로 섹션 바로 위에 배치)
query = st.text_input("", placeholder="🔍 무엇이든 검색하세요 (영화, 무협, 판타지...)", label_visibility="collapsed")

# -------------------------------------------------------------------------
# 메인 화면 구성
# -------------------------------------------------------------------------
if not query:
    # 1. 히어로 배너 (검색 전 첫인상)
    if os.path.exists(HERO_IMAGE_PATH):
        st.image(HERO_IMAGE_PATH, use_container_width=True)
    
    # 2. 실시간 인기 섹션 (트렌드)
    st.markdown("<div class='section-title'>🔥 지금 모두가 보고 있는 콘텐츠</div>", unsafe_allow_html=True)
    
    trending = fetch_data("/trending/all/day")
    if trending and "results" in trending:
        t_cols = st.columns(5)
        for i, item in enumerate(trending["results"][:10]):
            with t_cols[i % 5]:
                title = item.get("title") or item.get("name")
                poster = item.get("poster_path")
                rating = item.get("vote_average", 0.0)
                
                st.markdown(f"<div class='content-card'>", unsafe_allow_html=True)
                if poster:
                    st.image(f"https://image.tmdb.org/t/p/w500{{poster}}", use_container_width=True)
                st.markdown(f"<div class='card-info'><b>{{title}}</b><br><span class='tag'>⭐ {{rating:.1f}}</span></div></div>", unsafe_allow_html=True)

else:
    # 검색 결과 화면
    if TMDB_API_KEY == "여기에_본인의_TMDB_API_키를_입력하세요":
        st.error("앗! 검색을 위해 TMDB API 키가 필요합니다. 코드 상단의 API 키를 확인해 주세요!")
    else:
        results = fetch_data("/search/multi", {{"query": query}})
        
        if results and "results" in results:
            st.markdown(f"<div class='section-title'>🔍 '{{query}}' 검색 결과</div>", unsafe_allow_html=True)
            res_cols = st.columns(4)
            
            for idx, item in enumerate(results["results"][:16]):
                with res_cols[idx % 4]:
                    title = item.get("title") or item.get("name")
                    poster = item.get("poster_path")
                    media_type = item.get("media_type")
                    rating = item.get("vote_average", 0.0)
                    origin_country = item.get("origin_country", [])
                    is_cdrama = "CN" in origin_country or "TW" in origin_country
                    
                    st.markdown(f"<div class='content-card'>", unsafe_allow_html=True)
                    if poster:
                        st.image(f"https://image.tmdb.org/t/p/w500{{poster}}", use_container_width=True)
                    
                    st.markdown("<div class='card-info'>", unsafe_allow_html=True)
                    st.markdown(f"<h4 style='margin:0;'>{{title}}</h4>", unsafe_allow_html=True)
                    
                    # 태그 로직
                    tag_html = f"<span class='tag'>⭐ {{rating:.1f}}</span>"
                    if is_cdrama:
                         tag_html += "<span class='tag' style='color:#ff8db2; border-color:#ff8db2;'>#중국드라마</span>"
                    st.markdown(tag_html, unsafe_allow_html=True)
                    
                    st.markdown("<div style='margin-top:15px;'>", unsafe_allow_html=True)
                    st.link_button("넷플릭스 시청", f"https://www.netflix.com/search?q={{title}}")
                    if is_cdrama:
                        st.link_button("아이치이 바로가기", f"https://www.iq.com/search?query={{title}}")
                    st.markdown("</div></div></div>", unsafe_allow_html=True)
        else:
            st.warning("검색 결과가 없네요. 다른 검색어를 입력해 보세요!")

# 푸터 (MZ 스타일)
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.divider()
st.caption("Developed by AI Mango 🫡🥈💎 - Premium OTT Collection v2.0")
