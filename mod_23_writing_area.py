import streamlit as st
import pandas as pd
import json
from io import BytesIO, StringIO
import base64
import docx
from docx import Document
from PIL import Image

# Ορισμός τίτλου σελίδας
st.set_page_config(
    page_title="Writing Area with Files",
    page_icon="📝",
    layout="wide"
)

# CSS για καλύτερη εμφάνιση
st.markdown("""
<style>
    .writing-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .toolbar-button {
        margin: 2px;
        padding: 5px 10px;
        border: 1px solid #ccc;
        border-radius: 3px;
        background: white;
        cursor: pointer;
    }
    .toolbar-button:hover {
        background: #f0f0f0;
    }
    .file-preview {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #eee;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

def read_docx(file):
    """Διαβάζει το περιεχόμενο από αρχείο DOCX"""
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def insert_text_at_cursor(text_to_insert):
    """Εισάγει κείμενο στο τρέχον cursor position"""
    if 'writing_content' not in st.session_state:
        st.session_state.writing_content = ""
    
    # Απλή προσθήκη στο τέλος (για τώρα)
    st.session_state.writing_content += text_to_insert + "\n"

def main_writing_area():
    st.title("📝 Writing Area")
    st.markdown("---")
    
    # Δημιουργία δύο columns
    col1, col2 = st.columns([4, 1], gap="small", vertical_alignment="top")
    
    with col1:
        st.markdown("### ✍️ Writing Editor")
        
        # Toolbar για rich text
        st.markdown('<div style="background:#f8f9fa; padding:10px; border-radius:5px 5px 0 0; border:1px solid #ddd; border-bottom:none;">', unsafe_allow_html=True)
        col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns(7)
        
        with col_t1:
            if st.button("**B**", help="Bold", key="btn_bold"):
                insert_text_at_cursor("**bold text**")
        with col_t2:
            if st.button("*I*", help="Italic", key="btn_italic"):
                insert_text_at_cursor("*italic text*")
        with col_t3:
            if st.button("H1", help="Heading 1", key="btn_h1"):
                insert_text_at_cursor("# Heading 1")
        with col_t4:
            if st.button("H2", help="Heading 2", key="btn_h2"):
                insert_text_at_cursor("## Heading 2")
        with col_t5:
            if st.button("📋", help="Bullet List", key="btn_list"):
                insert_text_at_cursor("- List item")
        with col_t6:
            if st.button("🔗", help="Link", key="btn_link"):
                insert_text_at_cursor("[Link text](https://example.com)")
        with col_t7:
            if st.button("📝", help="Clear", key="btn_clear"):
                st.session_state.writing_content = ""
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Κύριο writing area
        if 'writing_content' not in st.session_state:
            st.session_state.writing_content = ""
        
        # Text area για γράψιμο
        writing_content = st.text_area(
            "Γράψτε εδώ...",
            value=st.session_state.writing_content,
            height=400,
            label_visibility="collapsed",
            key="writing_area_main"
        )
        
        # Αποθήκευση περιεχομένου
        st.session_state.writing_content = writing_content
        
        # Προβολή με μορφοποίηση
        st.markdown("---")
        st.markdown("### 📋 Preview")
        if st.session_state.writing_content:
            st.markdown(st.session_state.writing_content)
        else:
            st.info("Start typing above to see preview...")
        
        # Quick stats
        if st.session_state.writing_content:
            words = len(st.session_state.writing_content.split())
            chars = len(st.session_state.writing_content)
            st.caption(f"📊 Words: {words} | Characters: {chars}")
    
    with col2:
        st.markdown("### 📁 Files")
        
        # Tab για διαφορετικούς τύπους αρχείων
        tab1, tab2 = st.tabs(["Upload", "Recent"])
        
        with tab1:
            # File uploader
            uploaded_files = st.file_uploader(
                "Choose files",
                type=['txt', 'docx', 'csv', 'json', 'jpg', 'png', 'pdf'],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
            
            if uploaded_files:
                st.success(f"📁 {len(uploaded_files)} files uploaded")
                
                # Προβολή λίστας αρχείων
                for file in uploaded_files:
                    with st.expander(f"📄 {file.name[:20]}...", expanded=False):
                        # Προσπάθεια προβολής αρχείου
                        try:
                            if file.name.endswith('.txt'):
                                content = file.read().decode('utf-8')
                                file.seek(0)
                                st.text_area("Content", content, height=150, key=f"txt_{file.name}")
                                
                            elif file.name.endswith('.docx'):
                                content = read_docx(file)
                                st.text_area("Content", content[:500], height=150, key=f"docx_{file.name}")
                                
                            elif file.name.endswith('.csv'):
                                df = pd.read_csv(file)
                                st.dataframe(df.head(5), use_container_width=True)
                                
                            elif file.name.endswith('.json'):
                                content = json.loads(file.read().decode('utf-8'))
                                file.seek(0)
                                st.json(content, expanded=False)
                                
                            elif file.name.endswith(('.jpg', '.png', '.jpeg')):
                                st.image(file, use_column_width=True)
                                
                            elif file.name.endswith('.pdf'):
                                st.info("PDF preview requires additional libraries")
                                # Download button
                                st.download_button(
                                    label="Download PDF",
                                    data=file,
                                    file_name=file.name,
                                    mime="application/pdf"
                                )
                                
                            # Κουμπί για προσθήκη περιεχομένου στο writing area
                            if st.button(f"Add to text", key=f"add_{file.name}"):
                                if file.name.endswith('.txt'):
                                    content = file.read().decode('utf-8')
                                    st.session_state.writing_content += "\n\n" + content
                                    st.rerun()
                                elif file.name.endswith('.docx'):
                                    content = read_docx(file)
                                    st.session_state.writing_content += "\n\n" + content
                                    st.rerun()
                                    
                        except Exception as e:
                            st.error(f"Error reading file: {str(e)}")
                            
            else:
                st.info("Upload files to preview")
        
        with tab2:
            if 'recent_files' not in st.session_state:
                st.session_state.recent_files = []
            
            if st.session_state.recent_files:
                for i, file_info in enumerate(st.session_state.recent_files[:3]):
                    st.write(f"{i+1}. {file_info}")
            else:
                st.info("No recent files")
        
        # Save options
        st.markdown("---")
        st.markdown("#### 💾 Save")
        
        if st.session_state.writing_content:
            filename = st.text_input("Filename", value="my_document.txt")
            
            if st.button("💾 Save as TXT", use_container_width=True):
                # Create download button
                st.download_button(
                    label="Download",
                    data=st.session_state.writing_content.encode(),
                    file_name=filename if filename.endswith('.txt') else filename + '.txt',
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.info("Write something to save")

# Εκτέλεση
if __name__ == "__main__":
    main_writing_area()