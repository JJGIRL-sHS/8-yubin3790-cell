from datetime import datetime
import streamlit as st
import pandas as pd

# ✅ 세션 상태 초기화 (가장 중요!)
if "sonar_sensor_data" not in st.session_state:
    st.session_state.sonar_sensor_data = []

if "sound_sensor_data" not in st.session_state:
    st.session_state.sound_sensor_data = []


@st.fragment(run_every="1s")
def display_data():
    col_sonar, col_sound = st.columns(2)

    # =======================
    # 📡 수액(초음파) 센서
    # =======================
    with col_sonar:
        st.subheader("수액 잔량")

        if len(st.session_state.sonar_sensor_data) > 0:
            df_sonar = pd.DataFrame(st.session_state.sonar_sensor_data)

            if "time" in df_sonar.columns:
                df_sonar = df_sonar.set_index("time")

            # 이동 평균 (초반에도 값 나오도록 개선)
            if "distance" in df_sonar.columns:
                df_sonar["distance_ma"] = df_sonar["distance"].rolling(
                    window=5, min_periods=1
                ).mean()

            plot_df_sonar = df_sonar.tail(60).copy()
            plot_df_sonar = plot_df_sonar[["distance", "distance_ma"]]
            plot_df_sonar = plot_df_sonar.rename(columns={
                "distance": "거리",
                "distance_ma": "이동 평균"
            })

            st.line_chart(
                plot_df_sonar,
                color=['#EEEEEE', "#58A4E7"],
                y_label="수액 잔량 (cm)"
            )

            current_value = df_sonar["distance"].values[-1]
            max_value = df_sonar["distance"].max()
            min_value = df_sonar["distance"].min()
            avg_value = df_sonar["distance"].mean()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("현재", current_value)
            m2.metric("최대", max_value)
            m3.metric("최소", min_value)
            m4.metric("평균", f"{avg_value:0.0f}")

            with st.expander("수액 센서 원본 데이터 보기"):
                st.dataframe(df_sonar.sort_index(ascending=False))
        else:
            st.info("수액 센서 데이터 없음")

    # =======================
    # 🔊 소리 센서
    # =======================
    with col_sound:
        st.subheader("이상 소음")

        if len(st.session_state.sound_sensor_data) > 0:
            df_sound = pd.DataFrame(st.session_state.sound_sensor_data)

            if "time" in df_sound.columns:
                df_sound = df_sound.set_index("time")

            plot_df_sound = df_sound.tail(60)

            st.line_chart(
                plot_df_sound,
                color="#C2D640",
                y_label="decibel"
            )

            current_value = df_sound["decibel"].values[-1]
            max_value = df_sound["decibel"].max()
            min_value = df_sound["decibel"].min()
            avg_value = df_sound["decibel"].mean()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("현재", current_value)
            m2.metric("최대", max_value)
            m3.metric("최소", min_value)
            m4.metric("평균", f"{avg_value:0.0f}")

            with st.expander("소리 센서 원본 데이터 보기"):
                st.dataframe(df_sound.sort_index(ascending=False))
        else:
            st.info("소리 센서 데이터 없음")


# 실행
display_data()