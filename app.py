import streamlit as st
import streamlit.components.v1 as components
from backend import get_bot_response, transcribe_audio

# ──────────────────────────────────────────────
# PAGE CONFIG — must be the very first st command
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="MindGuide AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────
# CUSTOM CSS — calming theme
# ──────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* ── Root Variables ── */
    :root {
        --primary: #4A90A4;
        --primary-light: #5BA3B5;
        --bg-dark: #0E1117;
        --card-bg: #1A1F2E;
        --text-primary: #E8ECF1;
        --text-secondary: #9CA3AF;
        --user-bubble: #2D5F7C;
        --bot-bubble: #1E293B;
        --danger: #DC3545;
        --warning: #F59E0B;
        --success: #10B981;
        --accent: #7C3AED;
    }

    /* ── Global Font ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
/* ── App Background Gradient (single fixed layer) ── */
html, body {
    background: linear-gradient(135deg, #060B2E 0%, #0A0A1F 55%, #05050C 100%) fixed !important;
    min-height: 100vh;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background: transparent fixed !important;
}


[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: transparent fixed !important;
    box-shadow: none !important;
}


/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #00001c !important;
}

    /* ── Hide Streamlit Defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stHeaderActionElements"] {display: none !important;}

    /* ── Sidebar Styling ── */
    [data-testid="stSidebar"] {
        background-color: #141824;
        border-right: 1px solid #1E293B;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* ── App Header ── */
    .app-header {
        text-align: center;
        padding: 0.3rem 0 1rem 0;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 800px !important;
}

    .app-header h1 {
        font-size: 1.8rem;
        font-weight: 600;
        color: #E8ECF1;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .app-header p {
        font-size: 0.95rem;
        color: #9CA3AF;
        margin: 0.3rem 0 0 0;
    }

    /* ── Chat Message Styling ── */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        margin-bottom: 0.5rem;
        padding: 0.75rem 1rem;
    }

    /* ── Chat Input Styling ── */
    [data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        border-radius: 12px;
    }

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    border: transparent !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"]:focus-within,
[data-testid="stChatInput"] > div:focus-within {
    box-shadow: 0 0 0 1px #FFFFFF !important;
}

[data-testid="stChatInput"] textarea {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
    
    /* ── Card Component ── */
    .mg-card {
        background-color: #000038;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border: 0.2px solid #00007d;
    }

    /* ── Crisis Banner ── */
    .crisis-banner {
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .crisis-banner.elevated {
        background-color: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #F59E0B;
    }

    .crisis-banner.high {
        background-color: rgba(220, 53, 69, 0.12);
        border: 1px solid rgba(220, 53, 69, 0.3);
        color: #DC3545;
    }

    .crisis-banner.imminent {
        background-color: rgba(220, 53, 69, 0.2);
        border: 2px solid rgba(220, 53, 69, 0.5);
        color: #FF6B6B;
        font-weight: 600;
    }

    /* ── Resource Card ── */
    .resource-card {
        background-color: #1A1F2E;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.4rem 0;
        border-left: 4px solid var(--primary);
    }

    .resource-card.emergency {
        border-left-color: #DC3545;
    }

    .resource-card.crisis {
        border-left-color: #F59E0B;
    }

    .resource-card.professional {
        border-left-color: #10B981;
    }

    .resource-card h4 {
        margin: 0 0 0.3rem 0;
        font-size: 0.95rem;
        color: #E8ECF1;
    }

    .resource-card p {
        margin: 0;
        font-size: 0.85rem;
        color: #9CA3AF;
    }

    /* ── Emotion Badge ── */
    .emotion-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        color: #9CA3AF;
        background-color: rgba(74, 144, 164, 0.15);
        border: 1px solid rgba(74, 144, 164, 0.25);
        margin-top: 0.3rem;
    }

    /* ── Coping Card ── */
    .coping-card {
        background: linear-gradient(135deg, #1A1F2E 0%, #1E2636 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #2A3040;
    }

    .coping-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 0.9rem;
        color: #5BA3B5;
    }

    .coping-card p {
        margin: 0;
        font-size: 0.85rem;
        color: #B0B8C4;
    }

    /* ── Button Styling ── */
    .stButton > button {
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }

.st-key-new_chat_btn button {
    background-color: #151e3d !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    color: #FFFFFF !important;
}

.st-key-new_chat_btn button:hover {
    background-color: #0d1329 !important;
    border-color: #ffffff !important;
}

.st-key-start_btn button {
    background-color: rgba(0, 0, 232, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    color: #FFFFFF !important;
}

.st-key-start_btn button:hover {
    background-color: #10186f !important;
    border-color: #FFFFFF !important;
}

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    /* ── Divider ── */
    .mg-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #2A3040, transparent);
        margin: 1rem 0;
    }

    /* ── Left-align sidebar chat list buttons ── */
    [data-testid="stSidebar"] .stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
    }

    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] textarea:focus-visible {
    outline: none !important;
    box-shadow: none !important;
    border-color: transparent !important;
}

    /* ── Active Chat Row (disabled button, styled to stand out) ── */
    [data-testid="stSidebar"] button:disabled {
        background-color: rgba(74, 144, 164, 0.18) !important;
        border: 1px solid rgba(74, 144, 164, 0.4) !important;
        color: #FFFFFF !important;
        opacity: 1 !important;
        cursor: default !important;
    }

    /* ── Delete icon next to the active chat — matches its highlight color ── */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(button:disabled) [data-testid="stButton"] button:not(:disabled) {
        background-color: rgba(74, 144, 164, 0.18) !important;
        border: 1px solid rgba(74, 144, 164, 0.4) !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(button:disabled) [data-testid="stButton"] button:not(:disabled):hover {
        background-color: rgba(74, 144, 164, 0.28) !important;
        border: 1px solid rgba(74, 144, 164, 0.55) !important;
    }

/* ── Voice Input (mic docked inside the chat input bar) ── */
    /* The mic is positioned by JS so it tracks the chat input at any window
       size and with the sidebar open or collapsed. These are fallback values. */
    [data-testid="stAudioInput"] {
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
        border: none !important;
        gap: 0 !important;
    }

    /* Strip the widget down to just its record button */
    [data-testid="stAudioInput"] label,
    [data-testid="stAudioInput"] [data-testid="stElementToolbar"],
    [data-testid="stAudioInput"] [data-testid="stAudioInputWaveSurfer"],
    [data-testid="stAudioInput"] [data-testid="stAudioInputWaveformTimeCode"] {
        display: none !important;
    }

    /* Inner wrapper keeps its own padding/margin — zero it so the button
       lines up exactly with the send arrow instead of touching it */
    [data-testid="stAudioInput"] > div > div {
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stAudioInput"] > div {
        width: 36px !important;
        height: 36px !important;
        min-height: 36px !important;
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        gap: 0 !important;
    }

    [data-testid="stAudioInputActionButton"] {
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        border-radius: 50% !important;
        background: transparent !important;
        color: #9CA3AF !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: background-color 0.15s ease, color 0.15s ease;
    }

    [data-testid="stAudioInputActionButton"]:hover {
        background-color: rgba(74, 144, 164, 0.18) !important;
        color: #5BA3B5 !important;
    }

    [data-testid="stAudioInputActionButton"] svg {
        width: 19px !important;
        height: 19px !important;
    }

    /* While recording, the button turns into a pulsing red stop control */
    [data-testid="stAudioInputActionButton"][aria-label*="top"] {
        color: #DC3545 !important;
        background-color: rgba(220, 53, 69, 0.15) !important;
        animation: mg-mic-pulse 1.4s ease-in-out infinite;
    }

    @keyframes mg-mic-pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.45); }
        50%      { box-shadow: 0 0 0 6px rgba(220, 53, 69, 0); }
    }

    /* Keep typed text from running underneath the mic */
    [data-testid="stChatInput"] textarea {
        padding-right: 46px !important;
    }

    /* The invisible helper component that positions the mic */
    [data-testid="stElementContainer"]:has(> [data-testid="stIFrame"][title="mg_mic_anchor"]) {
        display: none !important;
    }

    /* ── Toast notifications — bottom-center, just above the chat bar ── */
    [data-testid="stToast"] {
        position: fixed !important;
        top: auto !important;
        bottom: 130px !important;
        left: 60% !important;
        right: auto !important;
        transform: translateX(-50%) !important;
    }

[class*="st-key-reaction_row_"] [data-testid="stHorizontalBlock"] {
    gap: 4px !important;
}

[class*="st-key-reaction_row_"] [data-testid="stColumn"] {
    width: fit-content !important;
    min-width: fit-content !important;
    flex: unset !important;
    padding: 0 !important;
}

[class*="st-key-reaction_row_"] button {
    background: transparent !important;
    border: none !important;
    padding: 0 4px !important;
    margin: 0 !important;
    min-height: unset !important;
    height: auto !important;
    font-size: 0.85rem !important;
    color: #9CA3AF !important;
    box-shadow: none !important;
}
[class*="st-key-reaction_row_"] button:hover {
    color: #E8ECF1 !important;
    background: rgba(255,255,255,0.05) !important;
}
[class*="st-key-reaction_row_"] button:disabled {
    opacity: 0.5 !important;
}



    </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧠 MindGuide AI")
        st.markdown(
            '<p style="color:#f0ead6; font-size:0.85rem;">'
            "Your safe space to talk</p>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="mg-divider"></div>', unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary", key="new_chat_btn"):
            sync_current_session()
            st.session_state.messages = []
            st.session_state.current_risk_level = "L0"
            import time, uuid
            st.session_state.session_start_time = time.time()
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

        st.markdown('<div class="mg-divider"></div>', unsafe_allow_html=True)
        
        # Past Chats Section
        st.markdown("#### 🕒 Past Chats")

        # Show ALL sessions — including the active one, which appears
        # the instant the first message is sent (Gemini/ChatGPT-style).
        all_sessions = st.session_state.past_sessions

        if all_sessions:
            for sid, data in reversed(list(all_sessions.items())):
                is_active = (sid == st.session_state.session_id)

                if st.session_state.renaming_sid == sid:
                    # ── Rename mode: text input + confirm/cancel ──
                    rcol1, rcol2, rcol3 = st.columns([3, 1, 1])
                    with rcol1:
                        new_title = st.text_input(
                            "Rename chat",
                            value=data["title"],
                            key=f"rename_input_{sid}",
                            label_visibility="collapsed",
                        )
                    with rcol2:
                        if st.button("✓", key=f"confirm_rename_{sid}", help="Save name"):
                            cleaned = new_title.strip()
                            if cleaned:
                                st.session_state.past_sessions[sid]["title"] = cleaned
                            st.session_state.renaming_sid = None
                            st.rerun()
                    with rcol3:
                        if st.button("✕", key=f"cancel_rename_{sid}", help="Cancel"):
                            st.session_state.renaming_sid = None
                            st.rerun()
                else:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if is_active:
                            # Same widget type as the others (disabled), so the
                            # box size, padding, and spacing match exactly.
                            st.button(
                                data['title'],
                                key=f"active_{sid}",
                                use_container_width=True,
                                disabled=True,
                            )
                        else:
                            if st.button(data['title'], key=f"load_{sid}", use_container_width=True):
                                sync_current_session()
                                st.session_state.messages = data["messages"]
                                st.session_state.current_risk_level = data["risk_level"]
                                st.session_state.session_id = sid
                                st.rerun()
                    with col2:
                        if st.button("✏️", key=f"rename_{sid}", help="Rename chat"):
                            st.session_state.renaming_sid = sid
                            st.rerun()
                    with col3:
                        if st.button("✕", key=f"del_{sid}", help="Delete chat"):
                            if sid in st.session_state.past_sessions:
                                del st.session_state.past_sessions[sid]

                            if is_active:
                                # Deleting the chat you're currently in also
                                # starts a fresh new conversation, since you
                                # can't be left with no active chat at all.
                                st.session_state.messages = []
                                st.session_state.current_risk_level = "L0"
                                import time, uuid
                                st.session_state.session_start_time = time.time()
                                st.session_state.session_id = str(uuid.uuid4())

                            st.toast("Chat deleted")
                            st.rerun()
        else:
            st.markdown("<p style='color:#9CA3AF; font-size:0.85rem;'>No past chats yet.</p>", unsafe_allow_html=True)
                    
        st.markdown('<div class="mg-divider"></div>', unsafe_allow_html=True)

        # About section
        with st.expander("ℹ️ About MindGuide"):
            st.markdown(
                "MindGuide is an **AI wellbeing companion** — not a therapist, "
                "diagnostic service, or emergency service. It helps you reflect, "
                "find coping strategies, and connect with professional resources."
            )

        # Emergency contacts — always visible
        with st.expander("🆘 Emergency Resources"):
            st.markdown("**Rescue 1122** (Punjab Emergency)")
            st.markdown("📞 `1122`")
            st.markdown("---")
            st.markdown("**Edhi Foundation**")
            st.markdown("📞 `115`")
            st.markdown("---")
            st.markdown("**Police Emergency**")
            st.markdown("📞 `15`")

        st.markdown('<div class="mg-divider"></div>', unsafe_allow_html=True)
            
        # Session duration info
        import time
        if "session_start_time" in st.session_state:
            mins_ago = int((time.time() - st.session_state.session_start_time) / 60)
            st.markdown(
                f'<p style="color:#2A3040; font-size:0.75rem; text-align:center; margin-top:2rem;">'
                f'Session started {mins_ago} min ago</p>',
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────
# APP HEADER
# ──────────────────────────────────────────────
def render_header():
    st.markdown(
        """
        <div class="app-header">
            <h1>🧠 MindGuide AI</h1>
            <p>Your safe space to talk — without judgment</p>
        </div>
        <div class="mg-divider"></div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# INITIALIZE SESSION STATE
# ──────────────────────────────────────────────
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_risk_level" not in st.session_state:
        st.session_state.current_risk_level = "L0"

    if "onboarded" not in st.session_state:
        st.session_state.onboarded = False
        
    if "session_id" not in st.session_state:
        # Generate a simple random session ID for the backend
        import uuid
        st.session_state.session_id = str(uuid.uuid4())

    if "session_start_time" not in st.session_state:
        import time
        st.session_state.session_start_time = time.time()
        
    if "past_sessions" not in st.session_state:
        # Keyed by session_id so each conversation only ever has ONE entry —
        # this also removes any chance of duplicate keys in the sidebar.
        st.session_state.past_sessions = {}
    elif isinstance(st.session_state.past_sessions, list):
        # Migrate old list-based sessions (from before this update) into
        # the new dictionary format, keyed by id.
        migrated = {}
        for sess in st.session_state.past_sessions:
            migrated[sess["id"]] = {
                "title": sess.get("title", "New Conversation"),
                "messages": sess.get("messages", []),
                "risk_level": sess.get("risk_level", "L0"),
            }
        st.session_state.past_sessions = migrated

    if "voice_nonce" not in st.session_state:
        # Bumped after each recording so the mic widget resets cleanly
        st.session_state.voice_nonce = 0
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False

    if "queued_inputs" not in st.session_state:
        st.session_state.queued_inputs = []

    if "feedback" not in st.session_state:
        st.session_state.feedback = {}          # idx -> "up" / "down"

    if "flagged_messages" not in st.session_state:
        st.session_state.flagged_messages = set()

    if "renaming_sid" not in st.session_state:
        st.session_state.renaming_sid = None

# ──────────────────────────────────────────────
# ONBOARDING SCREEN
# ──────────────────────────────────────────────
def render_onboarding():
    st.markdown("""
<div style="background-color: #000038; padding: 0.6rem 2rem 1rem 2rem; border-radius: 14px; border: 0.2px solid #00007d; margin-top: 1rem; margin-bottom: 1.5rem;">
    <h2 style="color: #82eefd; text-align: center; margin-bottom: 0.1rem; margin-top: 0;">Welcome to MindGuide!</h2>
    <p style="text-align: center; color: #f0ead6; margin-bottom: 0;">Your safe space to talk</p>
</div>
""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
<div class="mg-card" style="height: 100%;">
    <h4 style="color: #5edc1f; margin-top: 0;">What MindGuide CAN do:</h4>
    <ul style="color: #f0ead6; font-size: 0.9rem; padding-left: 1.2rem; margin-bottom: 0;">
        <li>Listen to you without judgment</li>
        <li>Suggest helpful coping techniques</li>
        <li>Connect you to professional help</li>
        <li>Respect your privacy and data</li>
    </ul>
</div>
""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
<div class="mg-card" style="height: 100%;">
    <h4 style="color: #F59E0B; margin-top: 0;">What MindGuide CANNOT do:</h4>
    <ul style="color: #f0ead6; font-size: 0.9rem; padding-left: 1.2rem; margin-bottom: 0;">
        <li>Diagnose any mental health conditions</li>
        <li>Replace human therapy or treatment</li>
        <li>Handle crisis emergencies alone</li>
        <li>Guarantee total confidentiality</li>
    </ul>
</div>
""", unsafe_allow_html=True)
        
    st.markdown("""
<p style="text-align: center; color: #9CA3AF; font-size: 0.85rem; margin-top: 0.8rem; margin-bottom: 0.5rem;">
    <em>Privacy Note: Guest mode is active — no account needed. You can delete your conversation history at any time using the sidebar.</em>
</p>
""", unsafe_allow_html=True)


    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("I understand, let's begin", use_container_width=True, type="primary", key="start_btn"):
            st.session_state.onboarded = True
            st.rerun()


# ──────────────────────────────────────────────
# MOCK BACKEND CALL (Temporary for testing)
# ──────────────────────────────────────────────
import time
def mock_backend_call(message, session_id):
    """Simulates the POST /chat API call to the backend."""
    time.sleep(1.5) # Simulate network delay
    
    # Simple keyword routing for our mock
    lower_msg = message.lower()
    if "kill" in lower_msg or "die" in lower_msg:
        return {
            "reply_text": "I hear how much pain you're in, and I want you to be safe. Please reach out to someone who can help right now.",
            "risk_level": "L3",
            "emotion": "overwhelmed",
            "resources": [{"name": "Rescue 1122", "phone": "1122", "type": "emergency"}],
            "coping_suggestions": []
        }
    elif "anxious" in lower_msg or "exam" in lower_msg:
        return {
            "reply_text": "Exams can be incredibly stressful. It's completely normal to feel this way. Let's try to take a step back and breathe.",
            "risk_level": "L0",
            "emotion": "anxious",
            "resources": [],
            "coping_suggestions": [{"title": "Box Breathing", "description": "Inhale for 4s, hold for 4s, exhale for 4s, hold for 4s.", "duration": "2 mins"}]
        }
    else:
        return {
            "reply_text": "Thank you for sharing that with me. I'm here to listen. How long have you been feeling this way?",
            "risk_level": "L0",
            "emotion": "neutral",
            "resources": [],
            "coping_suggestions": []
        }

# ──────────────────────────────────────────────
# HELPER: Keep the active conversation synced into history in real time
# ──────────────────────────────────────────────
def sync_current_session():
    """
    Mirrors the currently active conversation into past_sessions after
    every message — not just when switching away from it. This way the
    sidebar always reflects the latest state immediately, with no delay.
    """
    if len(st.session_state.messages) > 1:
        title = "New Conversation"
        for m in st.session_state.messages:
            if m["role"] == "user":
                title = m["content"][:20] + "..."
                break
        st.session_state.past_sessions[st.session_state.session_id] = {
            "title": title,
            "messages": st.session_state.messages,
            "risk_level": st.session_state.current_risk_level,
        }


# ──────────────────────────────────────────────
# HELPER: Process a message (from voice OR text) the same way
# ──────────────────────────────────────────────
def process_user_message(user_input):
    """
    Handles a user message end-to-end: appends it, calls the backend,
    and appends the assistant's reply. Used by both text and voice input,
    so the logic only needs to exist once.
    """
    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message instantly
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Show loading spinner
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("MindGuide is listening..."):
            try:
                # Pass recent chat history (before this new message) so the bot has context
                history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                    if m["role"] in ("user", "assistant")
                ]
                response = get_bot_response(user_input, history=history)

                # Update global risk level if it escalated
                if response["risk_level"] > st.session_state.current_risk_level:
                    st.session_state.current_risk_level = response["risk_level"]

                # Append assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["reply_text"],
                    "risk_level": response["risk_level"],
                    "emotion": response.get("emotion"),
                    "resources": response.get("resources", []),
                    "coping_suggestions": response.get("coping_suggestions", [])
                })
            except Exception as e:
                st.error("I'm having trouble connecting right now. If you need immediate help, please call Rescue 1122.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I'm having trouble connecting right now. If you need immediate help, please call Rescue 1122.",
                    "risk_level": "L0",
                    "emotion": None,
                    "resources": [],
                    "coping_suggestions": []
                })

    sync_current_session()
    st.rerun()

# ──────────────────────────────────────────────
# AUTOFOCUS — keeps the cursor in the chat input, no click needed
# ──────────────────────────────────────────────
def autofocus_chat_input():
    """
    Puts the cursor inside the chat textarea automatically on every
    render, so the user can start typing straight away without
    clicking into the box first.
    """
    components.html(
        """
<script>
(function () {
    const doc = window.parent.document;

    // Hide this helper iframe, same trick as the mic anchor.
    try {
        const frame = window.frameElement;
        if (frame) {
            frame.setAttribute("title", "mg_focus_anchor");
            const holder = frame.closest('[data-testid="stElementContainer"]');
            if (holder) {
                holder.style.display = "none";
            }
        }
    } catch (e) {}

    function focusChatInput() {
        const textarea = doc.querySelector(
            '[data-testid="stChatInput"] textarea'
        );

        if (!textarea) return;

        // Don't steal focus if the user is already typing somewhere
        // else on purpose (e.g. another text field).
        const active = doc.activeElement;
        const isTypingElsewhere =
            active &&
            active !== textarea &&
            (active.tagName === "TEXTAREA" || active.tagName === "INPUT");

        if (!isTypingElsewhere) {
            textarea.focus();
        }
    }

    // Try right away, then a couple more times shortly after —
    // Streamlit sometimes finishes rendering the chat input a
    // beat after this script runs.
    focusChatInput();
    setTimeout(focusChatInput, 150);
    setTimeout(focusChatInput, 400);
})();
</script>
        """,
        height=0,
        width=0,
    )

# ──────────────────────────────────────────────
# MIC DOCKING — keeps the mic inside the chat input bar
# ──────────────────────────────────────────────
def dock_mic_to_chat_input():
    """
    Keeps the native audio-input mic positioned inside the chat input.

    The mic position is continuously recalculated from the actual
    chat-input position, so it follows sidebar open/close, resizing,
    and other Streamlit layout changes.
    """
    components.html(
        """
<script>
(function () {
    const doc = window.parent.document;

    // This iframe is only a helper for positioning the mic.
    // Hide it completely.
    try {
        const frame = window.frameElement;

        if (frame) {
            frame.setAttribute("title", "mg_mic_anchor");

            const holder =
                frame.closest('[data-testid="stElementContainer"]');

            if (holder) {
                holder.style.display = "none";
            }
        }
    } catch (e) {}

    const SIZE = 36;
    const GAP = 6;

    function place() {
        const mic = doc.querySelector(
            '[data-testid="stAudioInput"]'
        );

        const chat = doc.querySelector(
            '[data-testid="stChatInput"]'
        );

        if (!mic || !chat) return;

        const box =
            mic.closest('[data-testid="stElementContainer"]') || mic;

        const chatRect = chat.getBoundingClientRect();

        if (!chatRect.width || !chatRect.height) return;

        const send =
            doc.querySelector(
                '[data-testid="stChatInputSubmitButton"]'
            );

        const sendRect =
            send ? send.getBoundingClientRect() : null;

        let right;

        if (sendRect && sendRect.width) {
            right = sendRect.left - GAP;
        } else {
            right = chatRect.right - 14;
        }

        /*
         * IMPORTANT:
         * Recalculate both LEFT and TOP every time.
         * This makes the mic follow the chat input when
         * Streamlit moves it after sidebar open/close.
         */
        const left = right - SIZE;

        const top =
            chatRect.top +
            (chatRect.height - SIZE) / 2;

        box.style.position = "fixed";
        box.style.zIndex = "1000";

        // Smooth transition so the mic slides along with the chat
        // bar instead of jumping instantly to its new position.
        box.style.transition = "left 0.000000000000000001s ease, top 0.000000000000000001s ease";

        box.style.width = SIZE + "px";
        box.style.height = SIZE + "px";

        box.style.minWidth = SIZE + "px";
        box.style.minHeight = SIZE + "px";

        box.style.margin = "0";
        box.style.padding = "0";

        box.style.left = left + "px";
        box.style.top = top + "px";
    }


    // Initial positioning
    place();


    /*
     * Recalculate when browser size changes.
     */
    window.parent.addEventListener("resize", place);


    /*
     * Sidebar opening/closing changes Streamlit's DOM.
     * Watch the entire Streamlit page for those changes.
     */
   

    if (doc.__mgMicMutationObserver) {
        doc.__mgMicMutationObserver.disconnect();
    }

    doc.__mgMicMutationObserver =
        new MutationObserver(function () {

            place();

            requestAnimationFrame(place);
            setTimeout(place, 50);
            setTimeout(place, 150);
            setTimeout(place, 300);
            setTimeout(place, 500);
        });

    doc.__mgMicMutationObserver.observe(
        doc.body,
        {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: [
                "style",
                "class",
                "aria-expanded"
            ]
        }
    );


    if (doc.__mgMicResizeObserver) {
        doc.__mgMicResizeObserver.disconnect();
    }

    doc.__mgMicResizeObserver =
        new ResizeObserver(function () {
            place();
        });

    doc.__mgMicResizeObserver.observe(doc.body);


    if (doc.__mgMicDockInterval) {
        clearInterval(doc.__mgMicDockInterval);
    }

    doc.__mgMicDockInterval =
        setInterval(place, 100);

})();
</script>
        """,
        height=0,
    )


# ──────────────────────────────────────────────
# SUBMIT GUARD — stops Enter/arrow from actually sending while busy
# ──────────────────────────────────────────────
def block_submit_while_busy():
    """
    Prevents the chat input from actually submitting (Enter key or the
    send arrow) while MindGuide is still generating a reply. Typing
    stays fully open — the message just doesn't go anywhere until the
    bot is free, so nothing gets lost or has to be retyped.
    """
    components.html(
        """
<script>
(function () {
    const doc = window.parent.document;

    try {
        const frame = window.frameElement;
        if (frame) {
            frame.setAttribute("title", "mg_submit_guard");
            const holder = frame.closest('[data-testid="stElementContainer"]');
            if (holder) holder.style.display = "none";
        }
    } catch (e) {}

    function isBusy() {
        return !!doc.querySelector('[data-testid="stSpinner"]');
    }

    function flashBlocked(textarea) {
        if (!textarea) return;
        textarea.style.transition = "box-shadow 0.15s ease";
        textarea.style.boxShadow = "0 0 0 2px rgba(220, 53, 69, 0.6)";
        setTimeout(function () {
            textarea.style.boxShadow = "";
        }, 350);
    }

    function onKeydown(e) {
        const textarea =
            e.target.closest &&
            e.target.closest('[data-testid="stChatInput"] textarea');
        if (!textarea) return;

        if (e.key === "Enter" && !e.shiftKey && isBusy()) {
            e.preventDefault();
            e.stopPropagation();
            flashBlocked(textarea);
        }
    }

    function onClick(e) {
        const btn =
            e.target.closest &&
            e.target.closest('[data-testid="stChatInputSubmitButton"]');
        if (!btn) return;

        if (isBusy()) {
            e.preventDefault();
            e.stopPropagation();
            flashBlocked(doc.querySelector('[data-testid="stChatInput"] textarea'));
        }
    }

    if (doc.__mgSubmitKeydown) {
        doc.removeEventListener("keydown", doc.__mgSubmitKeydown, true);
    }
    if (doc.__mgSubmitClick) {
        doc.removeEventListener("click", doc.__mgSubmitClick, true);
    }

    doc.__mgSubmitKeydown = onKeydown;
    doc.__mgSubmitClick = onClick;

    doc.addEventListener("keydown", onKeydown, true);
    doc.addEventListener("click", onClick, true);
})();
</script>
        """,
        height=0,
        width=0,
    )


def detect_reply_lang(text):
    if not text:
        return "en"
    if any('\u0600' <= ch <= '\u06FF' for ch in text):
        return "ur"
    roman_words = {"hai","hain","kya","kaisay","kaise","ap","aap","tum","mein",
                   "main","ho","raha","rahi","rha","rhi","nahi","nahin","acha",
                   "theek","thik","kr","kro","plz","jldi","bs","na","wo","ye",
                   "yeh","chor","dekho","kese","kesay","krna"}
    if roman_words & set(text.lower().split()):
        return "roman_ur"
    return "en"

def get_prev_user_text(idx):
    for i in range(idx - 1, -1, -1):
        if st.session_state.messages[i]["role"] == "user":
            return st.session_state.messages[i]["content"]
    return ""

THUMBS_UP_REPLIES = {
    "en": "I'm really glad that helped 😊 Feel free to keep sharing whatever's on your mind.",
    "roman_ur": "Ye sun kar khushi hui 😊 Aap jo bhi share karna chahein, be-jhijhak batayein.",
    "ur": "یہ سن کر خوشی ہوئی 😊 آپ جو بھی دل میں ہے، بلا جھجک بتائیں۔",
}

THUMBS_DOWN_REPLIES = {
    "en": "I'm sorry that response didn't land well. Tell me more about what you needed and I'll try again.",
    "roman_ur": "Maazrat, wo jawab thek nahi laga. Batayein aap ko asal mein kis tarha ki baat chahiye thi, mein dobara koshish karta hun.",
    "ur": "معذرت، وہ جواب مناسب نہیں لگا۔ بتائیں آپ کو کس طرح کی بات چاہیے تھی، میں دوبارہ کوشش کرتا ہوں۔",
}

# ──────────────────────────────────────────────
# CHAT INTERFACE
# ──────────────────────────────────────────────
def render_chat_interface():
    # ── Crisis Banner ──
    current_risk = st.session_state.current_risk_level
    if current_risk == "L1":
        st.markdown('<div class="crisis-banner elevated">⚠️ If you\'re struggling, talking to someone you trust can help.</div>', unsafe_allow_html=True)
    elif current_risk == "L2":
        st.markdown('<div class="crisis-banner high">🚨 Your safety matters. Please consider reaching out to a crisis helpline.</div>', unsafe_allow_html=True)
    elif current_risk == "L3":
        st.markdown('<div class="crisis-banner imminent">🆘 If you\'re in immediate danger, please call Rescue 1122 or go to your nearest emergency room.</div>', unsafe_allow_html=True)

    # Initial Greeting
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hi there 👋 I'm MindGuide. I'm here to listen, without judgment. Whatever you're feeling right now — it's okay to share. What's on your mind?",
            "risk_level": "L0",
            "emotion": None,
            "resources": [],
            "coping_suggestions": []
        })

    # Render Chat History
    for idx, msg in enumerate(st.session_state.messages):
        avatar = "👤" if msg["role"] == "user" else "🧠"

        with st.chat_message(msg["role"], avatar=avatar):
            if msg["role"] == "assistant" and msg.get("risk_level") in ["L2", "L3"]:
                st.markdown(f'<div style="border-left: 3px solid #DC3545; padding-left: 10px;">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])

            if msg.get("resources"):
                for res in msg["resources"]:
                    r_type = res.get("type", "professional").lower()
                    st.markdown(f"""
<div class="resource-card {r_type}">
    <h4>{res.get('name')}</h4>
    <p>📞 <a href="tel:{res.get('phone')}" style="color: #9CA3AF; text-decoration: none;">{res.get('phone')}</a></p>
</div>
""", unsafe_allow_html=True)

            if msg.get("emotion") and msg["emotion"] != "neutral":
                st.markdown(f'<span class="emotion-badge">💭 Sensing: {msg["emotion"]} (estimate)</span>', unsafe_allow_html=True)

            if msg.get("coping_suggestions"):
                for cope in msg["coping_suggestions"]:
                    with st.expander(f"🌱 Try this: {cope.get('title')} ({cope.get('duration', 'quick')})"):
                        st.markdown(f"""
<div class="coping-card">
    <h4>{cope.get('title')}</h4>
    <p>{cope.get('description')}</p>
</div>
""", unsafe_allow_html=True)

            if msg["role"] == "assistant":
                fb = st.session_state.feedback.get(idx)
                flagged = idx in st.session_state.flagged_messages

                with st.container(key=f"reaction_row_{idx}"):
                    c1, c2, c3, _ = st.columns([1, 1, 2, 8])
                    with c1:
                        if st.button("👍", key=f"up_{idx}", help="Helpful", disabled=(fb is not None)):
                            st.session_state.feedback[idx] = "up"
                            lang = detect_reply_lang(get_prev_user_text(idx))
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": THUMBS_UP_REPLIES[lang],
                                "risk_level": "L0", "emotion": None,
                                "resources": [], "coping_suggestions": []
                            })
                            st.rerun()
                    with c2:
                        if st.button("👎", key=f"down_{idx}", help="Not helpful", disabled=(fb is not None)):
                            st.session_state.feedback[idx] = "down"
                            lang = detect_reply_lang(get_prev_user_text(idx))
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": THUMBS_DOWN_REPLIES[lang],
                                "risk_level": "L0", "emotion": None,
                                "resources": [], "coping_suggestions": []
                            })
                            st.rerun()
                    with c3:
                        label = "🚩 Flagged" if flagged else "⚠️ Flag"
                        if st.button(label, key=f"flag_{idx}", help="Flag as unsafe", disabled=flagged):
                            st.session_state.flagged_messages.add(idx)
                            st.toast("Message flagged for review. Thank you.", icon="⚠️")
                            st.rerun()

    # ── Voice Input (native mic widget, docked inside the chat input bar) ──
    # The widget key carries a nonce so it resets to a fresh mic after every
    # recording — otherwise it stays stuck showing the previous playback.
    if st.session_state.get("voice_error"):
        st.error(st.session_state.pop("voice_error"))

    audio_value = st.audio_input(
        "Voice input",
        label_visibility="collapsed",
        key=f"voice_recorder_{st.session_state.voice_nonce}",
    )
    dock_mic_to_chat_input()
    autofocus_chat_input()
    block_submit_while_busy()

    if audio_value is not None:
        # Retire this widget instance so the next rerun shows an empty mic
        st.session_state.voice_nonce += 1

        with st.spinner("Transcribing your voice..."):
            transcribed_text = transcribe_audio(audio_value)

        if transcribed_text:
            process_user_message(transcribed_text)
        else:
            st.session_state.voice_error = (
                "Sorry, couldn't transcribe that. Please try again or type instead."
            )
            st.rerun()


    # ── Text Input (native, always typable — submission itself is
    # blocked client-side by block_submit_while_busy() while a reply
    # is loading, so nothing gets lost or cancelled mid-flight) ──
    user_input = st.chat_input("Share what's on your mind...")

    if user_input:
        st.session_state.is_generating = True
        try:
            process_user_message(user_input)
        finally:
            st.session_state.is_generating = False
        st.rerun()

# ──────────────────────────────────────────────
# MAIN APP
# ──────────────────────────────────────────────
def main():
    # Load CSS theme
    load_css()

    # Initialize session state
    init_session_state()

    # Render sidebar
    render_sidebar()

    # Render header
    render_header()

    # Route based on onboarding status
    if not st.session_state.onboarded:
        render_onboarding()
    else:
        render_chat_interface()


if __name__ == "__main__":
    main()
