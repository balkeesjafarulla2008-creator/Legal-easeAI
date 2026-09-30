import os
import requests
import streamlit as st
from dotenv import load_dotenv

from utils.formatting import sanitize_text
from utils.document_utils import format_docx, format_pdf

# Load Environment Variables
load_dotenv()

# FastAPI Backend is running on port 8001
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8001"
)

# Page Configuration
st.set_page_config(
    page_title="LegalEase - AI Legal Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .sub-header {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 20px;
    }

    .legal-card {
        background-color: #0F172A;
        color: #F8FAFC;
        padding: 25px;
        border-radius: 8px;
        border-left: 5px solid #3B82F6;
        font-family: 'Courier New', Courier, monospace;
        white-space: pre-wrap;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        max-height: 600px;
        overflow-y: auto;
    }

    .disclaimer-box {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        color: #991B1B;
        padding: 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "edited_document" not in st.session_state:
    st.session_state.edited_document = ""

if "doc_type" not in st.session_state:
    st.session_state.doc_type = "Agreement"

if "terms_raw" not in st.session_state:
    st.session_state.terms_raw = ""

# Application Header
col_title, col_logo = st.columns([4, 1])

with col_title:
    st.markdown(
        '<div class="main-header">LegalEase</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-header">AI-Powered Legal Document Generator</div>',
        unsafe_allow_html=True
    )

with col_logo:
    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        st.image(logo_path, width=100)
    else:
        st.markdown("⚖️ **LegalEase AI**")

st.divider()

# Main Layout
col_left, col_right = st.columns([1, 1], gap="large")

# LEFT SIDE
with col_left:

    st.subheader("1. Document Parameters")

    doc_type_option = st.selectbox(
        "Document Type*",
        options=[
            "Agreement",
            "Contract",
            "NDA",
            "Lease Agreement",
            "Employment Offer Letter",
            "Freelance Work Contract",
            "Other"
        ]
    )

    if doc_type_option == "Other":

        custom_doc_type = st.text_input(
            "Specify Document Type*",
            value="General Agreement"
        )

        selected_doc_type = custom_doc_type

    else:
        selected_doc_type = doc_type_option

    parties_input = st.text_area(
        "Parties Involved*",
        placeholder="e.g., Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=100
    )

    terms_input = st.text_area(
        "Terms & Conditions (Separate terms using semicolons)*",
        placeholder="Payment within 30 days; Confidentiality must be maintained; Delivery by agreed deadline",
        height=150
    )

    dates_input = st.text_input(
        "Effective Date*",
        value="September 29, 2026"
    )

    generate_btn = st.button(
        "🚀 Generate Document",
        type="primary",
        use_container_width=True
    )

    if generate_btn:

        # Form Validation
        if not parties_input.strip():

            st.error("Please specify the parties involved.")

        elif not terms_input.strip():

            st.error("Please enter at least one term or condition.")

        elif not dates_input.strip():

            st.error("Please specify an effective date.")

        else:

            with st.spinner(
                "Drafter AI is synthesizing your legal document..."
            ):

                payload = {
                    "document_type": selected_doc_type,
                    "parties": parties_input,
                    "terms": terms_input,
                    "dates": dates_input
                }

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=45
                    )

                    if response.status_code == 200:

                        data = response.json()

                        generated_txt = data.get(
                            "document",
                            ""
                        )

                        st.session_state.generated_document = generated_txt
                        st.session_state.edited_document = generated_txt
                        st.session_state.doc_type = selected_doc_type
                        st.session_state.terms_raw = terms_input

                        st.success(
                            "Document generated successfully!"
                        )

                    else:

                        try:
                            err_detail = response.json().get(
                                "detail",
                                "Generation failed."
                            )
                        except Exception:
                            err_detail = response.text

                        st.error(
                            f"Backend Error: {err_detail}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI backend. "
                        "Make sure FastAPI is running on port 8001."
                    )

                except Exception as ex:

                    st.error(
                        f"An unexpected error occurred: {str(ex)}"
                    )


# RIGHT SIDE
with col_right:

    st.subheader("2. Review & Edit")

    if st.session_state.edited_document:

        tab_preview, tab_edit = st.tabs(
            ["📄 Document Preview", "✏️ Edit Text"]
        )

        # Preview
        with tab_preview:

            st.markdown(
                f'<div class="legal-card">'
                f'{st.session_state.edited_document}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Edit
        with tab_edit:

            updated_text = st.text_area(
                "Modify legal draft content directly:",
                value=st.session_state.edited_document,
                height=450
            )

            if updated_text != st.session_state.edited_document:

                st.session_state.edited_document = updated_text

        # Export
        st.subheader("3. Export Document")

        col_txt, col_docx, col_pdf = st.columns(3)

        # TXT
        with col_txt:

            st.download_button(
                label="📥 Download TXT",
                data=st.session_state.edited_document,
                file_name="LegalEase_Document.txt",
                mime="text/plain",
                use_container_width=True
            )

        # DOCX
        with col_docx:

            try:

                docx_bytes = format_docx(
                    text=st.session_state.edited_document,
                    doc_type=st.session_state.doc_type,
                    terms_raw=st.session_state.terms_raw
                )

                st.download_button(
                    label="📄 Download DOCX",
                    data=docx_bytes,
                    file_name="LegalEase_Document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"DOCX error: {str(e)}"
                )

        # PDF
        with col_pdf:

            try:

                pdf_bytes = format_pdf(
                    text=st.session_state.edited_document,
                    doc_type=st.session_state.doc_type
                )

                st.download_button(
                    label="📕 Download PDF",
                    data=pdf_bytes,
                    file_name="LegalEase_Document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"PDF error: {str(e)}"
                )

    else:

        st.info(
            "Fill out the document parameters on the left "
            "and click 'Generate Document' to view the output."
        )


# Legal Disclaimer
st.markdown("""
<div class="disclaimer-box">
    <strong>⚖️ LEGAL DISCLAIMER:</strong>
    This document is an AI-generated draft created for educational
    and informational purposes only. It does not constitute formal
    legal advice. Before executing or relying on this document,
    it must be reviewed and customized by a qualified legal
    professional in your jurisdiction.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    "<p style='text-align: center; color: #9CA3AF; "
    "font-size: 0.8rem;'>"
    "LegalEase Project © 2026 — Final Year Engineering Capstone"
    "</p>",
    unsafe_allow_html=True
)