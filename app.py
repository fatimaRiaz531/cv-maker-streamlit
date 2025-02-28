import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

# Function to generate PDF
def create_pdf(name, father_name, dob, cnic, email, phone, address, about, education, experience, skills, projects, certifications, hobbies, profile_image, style, color_theme):
    pdf = FPDF()
    pdf.add_page()

    # Calculate content length to adjust font size dynamically
    content_length = sum(map(len, [about, education, experience, skills, projects, certifications, hobbies]))
    if content_length > 800:
        content_size = 8
    elif content_length > 600:
        content_size = 9
    else:
        content_size = 10

    # Define fonts, sizes, and layouts based on style
    if style == "Office Job":
        font_style = "Times"
        title_size = 16
        section_size = 12
        layout = "formal"
        primary_color = (0, 0, 139)
        secondary_color = (0, 0, 0)
    elif style == "Developer":
        font_style = "Courier"
        title_size = 14
        section_size = 11
        layout = "technical"
        primary_color = (0, 128, 0)
        secondary_color = (0, 0, 0)
    elif style == "Creative":
        font_style = "Helvetica"
        title_size = 18
        section_size = 13
        layout = "creative"
        primary_color = (255, 69, 0)
        secondary_color = (0, 0, 0)

    # Title
    pdf.set_font(font_style, 'B', size=title_size)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 10, txt="Curriculum Vitae", ln=True, align='C')
    pdf.ln(5)

    # Profile Image
    if profile_image:
        pdf.image(profile_image, x=170, y=10, w=30, h=30)

    # Personal Information
    pdf.set_font(font_style, 'B', size=section_size)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 10, txt="Personal Information", ln=True)
    pdf.set_font(font_style, size=content_size)
    pdf.set_text_color(*secondary_color)
    pdf.cell(0, 5, txt=f"Name: {name}", ln=True)
    pdf.cell(0, 5, txt=f"Father's Name: {father_name}", ln=True)
    pdf.cell(0, 5, txt=f"Date of Birth: {dob}", ln=True)
    pdf.cell(0, 5, txt=f"CNIC: {cnic}", ln=True)
    pdf.cell(0, 5, txt=f"Email: {email}", ln=True)
    pdf.cell(0, 5, txt=f"Phone: {phone}", ln=True)
    pdf.cell(0, 5, txt=f"Address: {address}", ln=True)
    pdf.ln(5)

    # About Me Section
    if about:
        pdf.set_font(font_style, 'B', size=section_size)
        pdf.set_text_color(*primary_color)
        pdf.cell(0, 10, txt="About Me", ln=True)
        pdf.set_font(font_style, size=content_size)
        pdf.set_text_color(*secondary_color)
        pdf.multi_cell(0, 5, txt=about)
        pdf.ln(5)

    # Section order based on style
    sections_order = {
        "formal": ["Education", "Experience", "Skills", "Projects", "Certifications", "Hobbies"],
        "technical": ["Skills", "Projects", "Experience", "Education", "Certifications", "Hobbies"],
        "creative": ["Hobbies", "Certifications", "Projects", "Skills", "Experience", "Education"]
    }[layout]

    for section in sections_order:
        data = locals().get(section.lower())
        if data:
            pdf.set_font(font_style, 'B', size=section_size)
            pdf.set_text_color(*primary_color)
            pdf.cell(0, 10, txt=section, ln=True)
            pdf.set_font(font_style, size=content_size)
            pdf.set_text_color(*secondary_color)
            for item in data.split("\n"):
                pdf.cell(0, 5, txt=f"- {item}", ln=True)
            pdf.ln(5)

    return pdf

# Streamlit App
st.title("Customizable CV Builder")
st.write("Create a professional CV tailored to your needs!")

style = st.selectbox("Select Resume Style", ["Office Job", "Developer", "Creative"])
color_theme = st.selectbox("Select Color Theme", ["Default Black", "Blue Theme", "Green Theme", "Red Theme"])

st.header("Personal Information")
name = st.text_input("Full Name")
father_name = st.text_input("Father's Name")
dob = st.text_input("Date of Birth (DD/MM/YYYY)")
cnic = st.text_input("CNIC Number")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
address = st.text_input("Address")
about = st.text_area("About Me (Optional)")

st.header("Sections")
education = st.text_area("Education (one entry per line)")
experience = st.text_area("Work Experience (one entry per line)")
skills = st.text_input("Skills (comma-separated)")
projects = st.text_area("Projects (optional, one entry per line)", value="")
certifications = st.text_area("Certifications (optional, one entry per line)", value="")
hobbies = st.text_input("Hobbies (optional, comma-separated)", value="")

profile_image = st.file_uploader("Upload Profile Picture (optional)", type=["jpg", "jpeg", "png"])

if st.button("Generate CV"):
    if name and father_name and dob and cnic and email and phone and address:
        image_path = None
        if profile_image:
            image = Image.open(profile_image)
            image_path = "profile_image.png"
            image.save(image_path)

        pdf = create_pdf(name, father_name, dob, cnic, email, phone, address, about, education, experience, skills, projects, certifications, hobbies, image_path, style, color_theme)

        pdf_file = "cv.pdf"
        pdf.output(pdf_file)

        with open(pdf_file, "rb") as f:
            st.download_button("Download Your CV", data=f, file_name="cv.pdf", mime="application/pdf")

        if image_path:
            os.remove(image_path)
    else:
        st.error("Please fill in all required fields.")

