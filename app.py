import streamlit as st

# Compatibilidad: el comando histórico ``streamlit run app.py`` debe abrir
# Aeraris y no el prototipo cripto anterior que se conservó en este archivo.
if __name__ == "__main__":
    from streamlit_app import main as aeraris_main

    aeraris_main()
    st.stop()
import random

# Configuración de la página
st.set_page_config(
    page_title="CryptoCopilot - Educación Cripto",
    page_icon="🪙",
    layout="wide"
)

# Estilos personalizados para principiantes (Fácil lectura)
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #1E3A8A; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.2rem; color: #4B5563; margin-bottom: 2rem; }
    .card { background-color: #F3F4F6; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid #3B82F6; }
    .danger-card { background-color: #FEF2F2; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid #EF4444; }
    .success-card { background-color: #ECFDF5; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid #10B981; }
</style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-title">🪙 CryptoCopilot Prototipo</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asistente educativo interactivo para principiantes absolutos en el mundo cripto.</div>', unsafe_allow_html=True)

# Inicializar estados de la sesión para interactividad
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "¡Hola! Soy tu Copiloto Cripto. Estoy aquí para explicarte cualquier concepto sin tecnicismos complejos. ¿Qué te gustaría aprender hoy?"}
    ]

# --- MENÚ LATERAL: CASOS DE USO ---
st.sidebar.title("🚀 Módulos del Copiloto")
modulo = st.sidebar.radio(
    "Selecciona un caso de uso para probar el prototipo:",
    ["1. Traductor ELI5 (Conceptos Difíciles)", "2. Simulador Anti-Estafas", "3. Chat de Consulta Simple"]
)

# --- CASO DE USO 1: TRADUCTOR ELI5 ---
if modulo == "1. Traductor ELI5 (Conceptos Difíciles)":
    st.header("🧠 Traductor ELI5 (Explícamelo como si tuviera 5 años)")
    st.write("Convierte términos intimidantes del ecosistema cripto en analogías del mundo real sencillas de entender.")
    
    termino = st.selectbox(
        "Elige un término técnico para ver cómo lo explicaría el Copiloto:",
        ["Blockchain (Cadena de bloques)", "Smart Contract (Contrato Inteligente)", "Frase Semilla / Clave Privada"]
    )
    
    if termino == "Blockchain (Cadena de bloques)":
        st.markdown("""
        <div class="card">
            <h4>🤖 Copiloto explica Blockchain:</h4>
            <p>Imagina un <b>libro de notas gigante y mágico</b> que está compartido en las computadoras de miles de personas en todo el mundo. Cada vez que alguien le envía dinero a otra persona, se anota en ese libro.</p>
            <p>Como todos tienen una copia exacta del mismo libro al mismo tiempo, <b>nadie puede hacer trampa</b>, borrar una página o inventar que tiene más dinero del que realmente tiene. ¡No necesitas un banco porque miles de testigos revisan que todo sea real!</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif termino == "Smart Contract (Contrato Inteligente)":
        st.markdown("""
        <div class="card">
            <h4>🤖 Copiloto explica Smart Contract:</h4>
            <p>Imagina una <b>máquina expendedora de refrescos</b>. Tú pones una moneda, presionas el botón de Coca-Cola y la máquina <i>automáticamente</i> te entrega la lata. No hay ningún cajero humano dentro de la máquina decidiendo si darte el refresco o quedarse con tu dinero.</p>
            <p>Un contrato inteligente es exactamente eso, pero hecho en código de computadora: un acuerdo que <b>se ejecuta solo</b> cuando se cumplen las reglas, sin intermediarios.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif termino == "Frase Semilla / Clave Privada":
        st.markdown("""
        <div class="card">
            <h4>🤖 Copiloto explica Frase Semilla:</h4>
            <p>Es la <b>llave maestra de tu caja fuerte</b>. Consiste en 12 o 24 palabras aleatorias (como <i>'gato, árbol, mesa...'</i>).</p>
            <p>Si pierdes tu computadora o celular, puedes poner esas palabras en cualquier otro dispositivo y recuperar todo tu dinero. Pero cuidado: <b>si alguien más ve estas palabras, puede robarte todo al instante</b>. Nunca se comparten con nadie.</p>
        </div>
        """, unsafe_allow_html=True)

# --- CASO DE USO 2: SIMULADOR ANTI-ESTAFAS ---
elif modulo == "2. Simulador Anti-Estafas":
    st.header("🛡️ Simulador Interactivo de Seguridad")
    st.write("Los principiantes suelen caer en trampas por falta de experiencia. Este módulo los entrena con escenarios reales simulados.")
    
    st.markdown("""
    <div class="danger-card">
        <h4>🚨 Alerta de Escenario Simulado:</h4>
        <p>Te unes a un grupo de soporte técnico en Telegram para resolver una duda con tu wallet. De inmediato, un usuario llamado <b>"Soporte_Oficial_Metamask"</b> te envía un mensaje privado diciendo:</p>
        <p><i>"Hola de parte del equipo de soporte. Para sincronizar tu cuenta y resolver tu problema rápidamente, por favor ingresa en este enlace seguro y escribe tus 12 palabras de recuperación."</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    opcion = st.radio(
        "¿Qué acción deberías tomar?",
        [
            "A) Hacer clic en el enlace para solucionar el problema rápido porque es soporte oficial.",
            "B) Bloquear al usuario inmediatamente y reportarlo, porque el soporte real nunca te pedirá tu frase semilla.",
            "C) Compartirle solo la mitad de las palabras para estar seguro."
        ]
    )
    
    if st.button("Validar Respuesta"):
        if opcion.startswith("B"):
            st.markdown("""
            <div class="success-card">
                <h4>¡Excelente! Respuesta Correcta. 🎉</h4>
                <p><b>Análisis del Copiloto:</b> El soporte técnico real de los proyectos cripto <b>NUNCA</b> te contactará por mensaje privado primero, y <b>JAMÁS</b> te pedirá tu frase semilla o contraseña. Esta es la estafa más común llamada <i>Phishing</i>.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="danger-card">
                <h4>❌ ¡Cuidado! Esa respuesta te haría perder tus fondos.</h4>
                <p><b>Análisis del Copiloto:</b> Los estafadores se hacen pasar por cuentas oficiales y crean páginas idénticas a las reales para robar tus datos. Si das tus palabras de recuperación, vaciarán tu billetera en segundos.</p>
            </div>
            """, unsafe_allow_html=True)

# --- CASO DE USO 3: CHAT DE CONSULTA SIMPLE ---
elif modulo == "3. Chat de Consulta Simple":
    st.header("💬 Chat con tu Copiloto")
    st.write("Un espacio limpio e intuitivo donde el principiante puede preguntar cualquier duda básica sin miedo a ser juzgado.")
    
    # Mostrar historial de chat existente
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Entrada del usuario
    if prompt := st.chat_input("Ej: ¿Cómo compro mi primer Bitcoin de forma segura?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Generar una respuesta simulada inteligente orientada a principiantes
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Respuestas simuladas basadas en palabras clave sencillas
            prompt_lower = prompt.lower()
            if "comprar" in prompt_lower or "compro" in prompt_lower:
                respuesta = "Para comprar de forma segura por primera vez, lo ideal es usar una plataforma de intercambio regulada y conocida (un 'Exchange' centralizado como Coinbase, Binance o Kraken). El proceso es similar a abrir una cuenta bancaria digital: te registras, verificas tu identidad con tu documento oficial y puedes comprar usando tu tarjeta de débito o transferencia bancaria local. ¡Empieza siempre con montos muy pequeños que no afecten tu economía!"
            elif "bitcoin" in prompt_lower and "que" in prompt_lower:
                respuesta = "Bitcoin es la primera criptomoneda del mundo. Imagínalo como 'oro digital'. Es un tipo de dinero completamente virtual que no depende de ningún gobierno ni banco central, lo que significa que nadie puede congelar tus fondos o imprimir más monedas de la nada para devaluarlo."
            else:
                respuesta = "¡Excelente pregunta! Recuerda que en el mundo cripto no es necesario comprar una moneda entera; puedes adquirir fracciones muy pequeñas (llamadas Satoshis en el caso de Bitcoin). El paso fundamental para un principiante es aprender a proteger su información antes de invertir dinero real."
                
            response_placeholder.write(respuesta)
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("CryptoCopilot educativo v1.0 • Diseñado específicamente para reducir la brecha de aprendizaje de manera segura.")
