import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="Kinetix: Next Generation Domotics", page_icon="🏠", layout="centered")

st.title("🏠 Kinetix: Next Generation Domotics")

# --- INIZIALIZZAZIONE DEGLI STATI ---
if "ruolo" not in st.session_state:
    st.session_state.ruolo = None

# Stati dispositivi base (accessibili a tutti)
if "stato_luci" not in st.session_state:
    st.session_state.stato_luci = "Spente"
if "stato_rafstors" not in st.session_state:
    st.session_state.stato_rafstors = "Giù"
if "stato_citofono" not in st.session_state:
    st.session_state.stato_citofono = "Chiuso"
if "stato_vmc" not in st.session_state:
    st.session_state.stato_vmc = "Velocità 1"

# Stati dispositivi sicurezza (solo Admin)
if "stato_allarme" not in st.session_state:
    st.session_state.stato_allarme = "Disinserito"
if "stato_porta_casa" not in st.session_state:
    st.session_state.stato_porta_casa = "Chiusa a chiave"

# --- SCHERMATA DI LOGIN ---
if st.session_state.ruolo is None:
    st.subheader("Accesso richiesto")
    password = st.text_input("Inserisci la password:", type="password")
    
    if st.button("Accedi", type="primary"):
        if password.lower() == "3033128875":
            st.session_state.ruolo = "admin"
            st.rerun()
        elif password.lower() == "utenteospite94)/67381268903#@]":  # <-- Cambia qui la password per l'utente standard
            st.session_state.ruolo = "utente"
            st.rerun()
        else:
            st.error("NON SEI AUTORIZZATO")

# --- PANNELLO DI CONTROLLO (DOPO IL LOGIN) ---
else:
    is_admin = (st.session_state.ruolo == "admin")

    col_titolo, col_esci = st.columns([4, 1])
    with col_titolo:
        if is_admin:
            st.success("Bentornato in Kinetix Danilo! (Amministratore)")
        else:
            st.info("Benvenuto in Kinetix! (Profilo Utente)")
    with col_esci:
        if st.button("Esci", use_container_width=True):
            st.session_state.ruolo = None
            st.rerun()

    # --- DASHBOARD STATO ATTUALE ---
    st.subheader("📊 Stato attuale della casa")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💡 Luci", st.session_state.stato_luci)
    m2.metric("🪟 Rafstors", st.session_state.stato_rafstors)
    m3.metric("🔔 Citofono", st.session_state.stato_citofono)
    m4.metric("💨 VMC", st.session_state.stato_vmc)

    # Se è Admin, mostra anche la riga con lo stato della sicurezza
    if is_admin:
        s1, s2 = st.columns(2)
        s1.metric("🚨 Allarme Casa", st.session_state.stato_allarme)
        s2.metric("🚪 Porta di Casa", st.session_state.stato_porta_casa)

    st.divider()
    st.write("Cosa desideri controllare?")

    # --- CREAZIONE SCHEDE IN BASE AL RUOLO ---
    if is_admin:
        tabs = st.tabs([
            "💡 Luci", 
            "🪟 Rafstors", 
            "🔔 Citofono", 
            "💨 VMC", 
            "🚨 Allarme", 
            "🚪 Porta Casa"
        ])
        tab_luci, tab_rafstors, tab_citofono, tab_vmc, tab_allarme, tab_porta = tabs
    else:
        tabs = st.tabs([
            "💡 Luci", 
            "🪟 Rafstors", 
            "🔔 Citofono", 
            "💨 VMC"
        ])
        tab_luci, tab_rafstors, tab_citofono, tab_vmc = tabs

    # 1. SEZIONE LUCI (Tutti)
    with tab_luci:
        st.subheader("Gestione Luci")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Accendi Luci (ON)", use_container_width=True):
                st.session_state.stato_luci = "Accese"
                st.rerun()
        with col2:
            if st.button("Spegni Luci (OFF)", use_container_width=True):
                st.session_state.stato_luci = "Spente"
                st.rerun()

    # 2. SEZIONE RAFSTORS (Tutti)
    with tab_rafstors:
        st.subheader("Gestione Rafstors")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Porta SU ⬆️", use_container_width=True):
                st.session_state.stato_rafstors = "Su"
                st.rerun()
        with col2:
            if st.button("Porta GIÙ ⬇️", use_container_width=True):
                st.session_state.stato_rafstors = "Giù"
                st.rerun()

    # 3. SEZIONE CITOFONO / PORTONE (Tutti)
    with tab_citofono:
        st.subheader("Gestione Citofono (Portone)")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔓 Apri Portone", use_container_width=True):
                st.session_state.stato_citofono = "Sbloccato"
                st.rerun()
        with col2:
            if st.button("📹 Vedi Telecamera", use_container_width=True):
                st.session_state.stato_citofono = "Video Aperto"
                st.rerun()
        with col3:
            if st.button("🔒 Chiudi / Reset", use_container_width=True):
                st.session_state.stato_citofono = "Chiuso"
                st.rerun()

    # 4. SEZIONE VMC (Tutti)
    with tab_vmc:
        st.subheader("Gestione VMC")
        indice_attuale = ["Velocità 1", "Velocità 2", "Velocità 3"].index(st.session_state.stato_vmc)
        velocita = st.radio(
            "A che velocità desideri mettere la VMC?",
            options=["1", "2", "3"],
            index=indice_attuale,
            horizontal=True
        )
        if st.button("Imposta Velocità VMC", type="primary"):
            st.session_state.stato_vmc = f"Velocità {velocita}"
            st.rerun()

    # 5 & 6. SEZIONI SICUREZZA (Solo Admin)
    if is_admin:
        with tab_allarme:
            st.subheader("Gestione Sistema d'Allarme")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛡️ Attiva Totale", use_container_width=True):
                    st.session_state.stato_allarme = "Attivo (Totale)"
                    st.rerun()
            with col2:
                if st.button("🌙 Attiva Notte", use_container_width=True):
                    st.session_state.stato_allarme = "Attivo (Notte)"
                    st.rerun()
            with col3:
                if st.button("🔕 Disinserisci", use_container_width=True):
                    st.session_state.stato_allarme = "Disinserito"
                    st.rerun()

        with tab_porta:
            st.subheader("Serratura Porta Blindata Casa")
            st.warning("⚠️ Controllo diretto sulla serratura dell'abitazione.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔓 Sblocca Porta Casa", type="primary", use_container_width=True):
                    st.session_state.stato_porta_casa = "Sbloccata"
                    st.rerun()
            with col2:
                if st.button("🔒 Chiudi a Chiave", use_container_width=True):
                    st.session_state.stato_porta_casa = "Chiusa a chiave"
                    st.rerun()
