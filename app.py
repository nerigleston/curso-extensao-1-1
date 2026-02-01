import base64
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI
from PIL import Image

load_dotenv()

st.set_page_config(page_title="AI Vision Comparison", page_icon="🤖", layout="wide")

HISTORY_FILE = "historico_interacoes.txt"


def process_with_gemini(image_bytes: bytes, mime_type: str, prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=[prompt, image_part]
    )

    return response.text


def process_with_openai(image_bytes: bytes, prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content


def save_interaction(
    image_name: str, prompt: str, gemini_response: str, openai_response: str
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"📅 Data/Hora: {timestamp}\n")
        f.write(f"🖼️  Imagem: {image_name}\n")
        f.write(f"❓ Pergunta: {prompt}\n")
        f.write("-" * 80 + "\n")
        f.write(f"🔷 GEMINI:\n{gemini_response}\n")
        f.write("-" * 80 + "\n")
        f.write(f"🟢 OPENAI:\n{openai_response}\n")
        f.write("=" * 80 + "\n\n")


def main():
    st.title("🤖 AI Vision Comparison")
    st.markdown(
        "Compare as respostas do **Gemini** e **OpenAI** na análise de imagens!"
    )

    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not gemini_key or not openai_key:
        st.error("⚠️ ERRO: API Keys não configuradas!")
        if not gemini_key:
            st.warning("❌ GEMINI_API_KEY não encontrada!")
        if not openai_key:
            st.warning("❌ OPENAI_API_KEY não encontrada!")
        st.info("Configure suas API keys no arquivo .env")
        st.code(
            """GEMINI_API_KEY=sua_chave_gemini_aqui
OPENAI_API_KEY=sua_chave_openai_aqui"""
        )
        st.stop()

    st.subheader("📤 Upload da Imagem")
    uploaded_file = st.file_uploader(
        "Escolha uma imagem",
        type=["png", "jpg", "jpeg", "webp", "heic", "heif"],
        help="Formatos suportados: PNG, JPEG, WEBP, HEIC, HEIF",
    )

    if uploaded_file:
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagem carregada", use_container_width=True)
            st.caption(
                f"📁 {uploaded_file.name} | 📏 {image.size[0]}x{image.size[1]}px"
            )

    st.subheader("💬 Sua Pergunta")
    prompt = st.text_area(
        "Digite sua pergunta ou instrução sobre a imagem:",
        height=100,
        placeholder="Ex: Descreva o que você vê nesta imagem em detalhes...",
        help="Seja específico para obter melhores respostas",
    )

    if st.button("🚀 Comparar Respostas", type="primary", use_container_width=True):
        if not uploaded_file:
            st.warning("⚠️ Por favor, faça upload de uma imagem primeiro!")
        elif not prompt:
            st.warning("⚠️ Por favor, digite uma pergunta ou instrução!")
        else:
            image_bytes = uploaded_file.getvalue()

            mime_types = {
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "webp": "image/webp",
                "heic": "image/heic",
                "heif": "image/heif",
            }
            extension = uploaded_file.name.lower().split(".")[-1]
            mime_type = mime_types.get(extension, "image/jpeg")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔷 Gemini")
                gemini_placeholder = st.empty()
                gemini_status = st.empty()

            with col2:
                st.subheader("🟢 OpenAI")
                openai_placeholder = st.empty()
                openai_status = st.empty()

            gemini_status.info("⏳ Processando com Gemini...")
            openai_status.info("⏳ Processando com OpenAI...")

            results = {"gemini": None, "openai": None}

            def run_gemini():
                try:
                    return (
                        "gemini",
                        process_with_gemini(image_bytes, mime_type, prompt),
                    )
                except Exception as e:
                    return ("gemini", f"ERRO: {str(e)}")

            def run_openai():
                try:
                    return ("openai", process_with_openai(image_bytes, prompt))
                except Exception as e:
                    return ("openai", f"ERRO: {str(e)}")

            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(run_gemini), executor.submit(run_openai)]

                for future in as_completed(futures):
                    model, result = future.result()
                    results[model] = result

                    if model == "gemini":
                        if result.startswith("ERRO:"):
                            gemini_status.error(f"❌ Erro no Gemini")
                            gemini_placeholder.error(result)
                        else:
                            gemini_status.success("✅ Gemini respondeu!")
                            gemini_placeholder.markdown(result)

                    elif model == "openai":
                        if result.startswith("ERRO:"):
                            openai_status.error(f"❌ Erro no OpenAI")
                            openai_placeholder.error(result)
                        else:
                            openai_status.success("✅ OpenAI respondeu!")
                            openai_placeholder.markdown(result)

            try:
                save_interaction(
                    uploaded_file.name, prompt, results["gemini"], results["openai"]
                )
                st.info(f"💾 Interação salva em: {HISTORY_FILE}")
            except Exception as e:
                st.warning(f"⚠️ Erro ao salvar histórico: {str(e)}")

    st.divider()

    if os.path.exists(HISTORY_FILE):
        with st.expander("📜 Ver Histórico de Interações"):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = f.read()
                st.text_area("Histórico", value=history, height=400, disabled=True)
            except Exception as e:
                st.error(f"Erro ao carregar histórico: {e}")

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        🔷 Google Gemini vs 🟢 OpenAI | Desenvolvido com Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
