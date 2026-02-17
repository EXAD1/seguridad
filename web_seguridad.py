from supabase import create_client, Client
import streamlit as st
import cv2
import numpy as np

# 1. Datos de conexión
URL_PROYECTO = "https://kofceetypfxcwxhvqsla.supabase.co"
LLAVE_API = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtvZmNlZXR5cGZ4Y3d4aHZxc2xhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5NDk1MDIsImV4cCI6MjA4NjUyNTUwMn0.hLcMPTCVHNzc4cJZdxzF60fH1vyRzCcQrtweNaCFM-4"

# 2. Conexión limpia (Sin parches, porque ya estarás en 3.12)
supabase: Client = create_client(URL_PROYECTO, LLAVE_API)

st.title("🎟️ Control de Acceso VIP")
token_ = st.text_input("Escanee el código QR del invitado")
archivo_subido = st.file_uploader("Sube la imagen del código QR", type=["png", "jpg"])

if archivo_subido is not None:
    # Convertimos la imagen subida a un formato que OpenCV entienda
    file_bytes = np.asarray(bytearray(archivo_subido.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # El detector busca el código
    detector = cv2.QRCodeDetector()
    token_leido, points, straight_qrcode = detector.detectAndDecode(opencv_image)

    if token_leido:
        st.info(f"Código detectado: {token_leido}")
        # AQUÍ LLAMAS A TU LÓGICA DE BÚSQUEDA USANDO token_leido
        token_ = token_leido  # Asignamos el token leído al input para su verificación
    respuesta = supabase.table("invitados").select("*").eq("token_qr", token_).execute()
    if len(respuesta.data) == 0:
        st.error("¡ERROR! Código no encontrado. Acceso denegado.")
    else:
        if respuesta.data[0]['ingresado']:
            st.error(f"Error: El invitado '{respuesta.data[0]['nombre']}' ya ha ingresado. Acceso denegado.")
        else:
            st.success(f"Invitado registrado {respuesta.data[0]['nombre']}! Puede pasar")
            col1, col2 = st.columns(2)
            invitado = respuesta.data[0]
            col1.metric("Invitado", invitado['nombre'])
            col2.metric("Vendedor", invitado['vendedor'])
            col1.metric("Token", invitado['token_qr'])
            col2.metric("Estado", "Pendiente")
            supabase.table("invitados").update({"ingresado": True}).eq("token_qr", token_).execute()
    

if st.button("Verificar Invitado"):
    st.write(f"Buscando el código: {token_}...")
    respuesta = supabase.table("invitados").select("*").eq("token_qr", token_).execute()
    if len(respuesta.data) == 0:
        st.error("¡ERROR! Código no encontrado. Acceso denegado.")
    else:
        if respuesta.data[0]['ingresado']:
            st.error(f"Error: El invitado '{respuesta.data[0]['nombre']}' ya ha ingresado. Acceso denegado.")
        else:
            st.success(f"Invitado registrado {respuesta.data[0]['nombre']}! Puede pasar")
            col1, col2 = st.columns(2)
            invitado = respuesta.data[0]
            col1.metric("Invitado", invitado['nombre'])
            col2.metric("Vendedor", invitado['vendedor'])
            col1.metric("Token", invitado['token_qr'])
            col2.metric("Estado", "Pendiente")
            supabase.table("invitados").update({"ingresado": True}).eq("token_qr", token_).execute()
    