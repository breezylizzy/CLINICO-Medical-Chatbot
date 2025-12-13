import streamlit as st
import uuid

from langchain_openai import ChatOpenAI
from src.chain import load_rag_chain

def normalize_query(query: str) -> str:
    mappings = {
        "infeksi ginjal": "kidney infection pyelonephritis",
        "radang ginjal": "pyelonephritis nephritis",
        "penyakit gula": "diabetes mellitus",
        "asam lambung": "GERD gastroesophageal reflux disease",
        "darah tinggi": "hypertension",
        "radang paru": "pneumonia",
        "sesak napas": "shortness of breath dyspnea",
        "nyeri dada": "chest pain"
    }

    q = query.lower()
    for k, v in mappings.items():
        if k in q:
            return v

    return query

@st.cache_resource
def load_chat_model(openai_key: str):
    return ChatOpenAI(
        openai_api_key=openai_key,
        model="gpt-4o-mini",
        temperature=0.0
    )

def main():
    st.set_page_config(
        page_title="CLINICO Medical Assistant",
        page_icon="🩺",
        layout="centered",
    )
    
    st.markdown("""
    <style>

        .stChatMessage.user {
            background: #0d3b66 !important;
            color: #e5f0ff !important;
            border-radius: 18px;
            padding: 12px 16px;
            margin: 10px 0;
            border: 1px solid rgba(229, 240, 255, 0.2) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        }

        .stChatMessage.assistant {
            background: rgba(255,255,255,0.06) !important;
            color: #e5f0ff !important;
            border-radius: 18px;
            padding: 12px 16px;
            margin: 10px 0;
            border: 1px solid rgba(255,255,255,0.1) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25);
            backdrop-filter: blur(4px);
        }

        .stChatInput > div > div {
            background: #0d3b66 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(229, 240, 255, 0.2) !important;
            box-shadow: 0 3px 6px rgba(0,0,0,0.35) !important;
            color: #e5f0ff !important;
        }

        input, textarea {
            background: transparent !important;
            color: #e5f0ff !important;
        }

        input::placeholder, textarea::placeholder {
            color: rgba(229, 240, 255, 0.4) !important;
        }

        .stApp {
            background: linear-gradient(
                to bottom,
                #000000 0%,
                #0a1a2a 40%,
                #0d3b66 60%,
                #000000 100%
            ) !important;
            background-attachment: fixed !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🩺 CLINICO - Medical Information Assistant")
    st.markdown(
        "CLINICO helps provide safe and informative health-related answers.  "
        "It does not give diagnoses or definitive medical prescriptions."
    )

    try:
        OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("Missing OPENAI_API_KEY in Streamlit secrets")

        chat_model = load_chat_model(OPENAI_API_KEY)
        rag_chain = load_rag_chain(chat_model)

        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I am CLINICO. How can I help you today?"
                }
            ]

    except Exception as e:
        st.error(f"Failed to initialize system: {e}")
        return
        
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
    if user_prompt := st.chat_input("Ask something about health..."):
        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )

        with st.chat_message("user", avatar="👤"):
            st.markdown(user_prompt)

        with st.spinner("CLINICO is thinking..."):
            try:
                normalized_prompt = normalize_query(user_prompt)

                response = rag_chain.invoke(
                    {
                        "input": normalized_prompt
                    },
                    config={
                        "configurable": {
                            "session_id": st.session_state.session_id
                        }
                    }
                )

                # IMPORTANT: do NOT override model output
                ai_text = response.get("answer", "")

                if not ai_text.strip():
                    ai_text = (
                        "I’m sorry, I couldn’t generate a response at this time. "
                        "Please try rephrasing your question."
                    )

            except Exception as e:
                ai_text = f"An error occurred while processing your request: {e}"

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_text}
        )

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(ai_text)

if __name__ == "__main__":
    main()
