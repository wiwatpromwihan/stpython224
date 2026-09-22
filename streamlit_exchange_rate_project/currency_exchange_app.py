import streamlit as st
import requests

st.set_page_config(
    page_title="Currency Exchange",
    page_icon="💱",
    layout="centered"
)

st.title("💱 โปรแกรมแปลงอัตราแลกเปลี่ยนเงินตรา")
st.caption("ข้อมูลอัตราแลกเปลี่ยนจาก ExchangeRate-API")

# เก็บ API Key ใน session เพื่อไม่ให้ต้องกรอกซ้ำทุกครั้งที่ Streamlit rerun
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input(
    "ExchangeRate-API Key",
    value=st.session_state.api_key,
    type="password",
    placeholder="กรอก API Key จาก exchangerate-api.com"
)
st.session_state.api_key = api_key.strip()

@st.cache_data(ttl=3600, show_spinner=False)
def get_supported_codes(api_key: str):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(data.get("error-type", "ไม่สามารถดึงรายการสกุลเงินได้"))

    return data["supported_codes"]

def convert_currency(api_key: str, base: str, target: str, amount: float):
    url = (
        f"https://v6.exchangerate-api.com/v6/{api_key}"
        f"/pair/{base}/{target}/{amount}"
    )
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(data.get("error-type", "ไม่สามารถแปลงสกุลเงินได้"))

    return data

if not api_key:
    st.info("กรุณากรอก API Key ก่อนใช้งาน")
    st.stop()

try:
    supported_codes = get_supported_codes(api_key)
    currency_names = {code: name for code, name in supported_codes}
    currency_codes = [code for code, _ in supported_codes]
except requests.RequestException as e:
    st.error(f"เชื่อมต่อ API ไม่สำเร็จ: {e}")
    st.stop()
except ValueError as e:
    st.error(f"API Error: {e}")
    st.stop()

def default_index(code):
    return currency_codes.index(code) if code in currency_codes else 0

amount = st.number_input(
    "จำนวนเงิน",
    min_value=0.0,
    value=1.0,
    step=1.0,
    format="%.2f"
)

col1, col2 = st.columns(2)

with col1:
    base_currency = st.selectbox(
        "จากสกุลเงิน",
        currency_codes,
        index=default_index("THB"),
        format_func=lambda c: f"{c} - {currency_names[c]}"
    )

with col2:
    target_currency = st.selectbox(
        "เป็นสกุลเงิน",
        currency_codes,
        index=default_index("USD"),
        format_func=lambda c: f"{c} - {currency_names[c]}"
    )

if st.button("คำนวณอัตราแลกเปลี่ยน", type="primary", use_container_width=True):
    if amount <= 0:
        st.warning("กรุณาระบุจำนวนเงินมากกว่า 0")
    else:
        try:
            with st.spinner("กำลังเรียกข้อมูลอัตราแลกเปลี่ยน..."):
                data = convert_currency(
                    api_key,
                    base_currency,
                    target_currency,
                    amount
                )

            rate = data["conversion_rate"]
            converted = data["conversion_result"]

            st.success(
                f"{amount:,.2f} {base_currency} = "
                f"{converted:,.4f} {target_currency}"
            )

            c1, c2 = st.columns(2)
            with c1:
                st.metric(
                    "อัตราแลกเปลี่ยน",
                    f"1 {base_currency} = {rate:,.6f} {target_currency}"
                )
            with c2:
                st.metric(
                    "จำนวนเงินหลังแปลง",
                    f"{converted:,.4f} {target_currency}"
                )

            last_update = data.get("time_last_update_utc")
            next_update = data.get("time_next_update_utc")

            if last_update:
                st.write(f"**อัปเดตล่าสุด:** {last_update}")
            if next_update:
                st.write(f"**อัปเดตครั้งถัดไป:** {next_update}")

        except requests.RequestException as e:
            st.error(f"เชื่อมต่อ API ไม่สำเร็จ: {e}")
        except ValueError as e:
            st.error(f"API Error: {e}")
        except KeyError:
            st.error("รูปแบบข้อมูลที่ได้รับจาก API ไม่ถูกต้อง")

st.divider()
st.caption(
    "หมายเหตุ: ต้องสมัครและนำ API Key จาก https://www.exchangerate-api.com/ มาใช้งาน"
)
