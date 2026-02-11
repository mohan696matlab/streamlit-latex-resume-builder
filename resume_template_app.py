import streamlit as st
import json
import os,shutil
from utlis import generate_latex_cv
import base64

pdf_path = "cv_cache/cv_output.pdf"

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="800px" 
            type="application/pdf">
        </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# Initialize session state for change tracking
if "last_cv_data" not in st.session_state:
    st.session_state.last_cv_data = None

# =====================================================
#                   PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Professional CV Builder",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
#                   HEADER
# =====================================================
st.title("🎯 Professional CV Builder")
st.markdown("""
<div class="info-box">
    <strong>Welcome!</strong> Create your professional CV by filling in the sections below. 
    Your data will be exported as a structured JSON file that you can use with CV templates or parsers.
</div>
""", unsafe_allow_html=True)

# =====================================================
#                   BASIC INFORMATION
# =====================================================
st.header("👤 Basic Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Full Name *",
        value="Balyogi Mohan Dash, PhD",
        placeholder="e.g., John Doe",
        help="Your full legal name"
    )

    job_title = st.text_input(
        "Job Title *",
        value="Computer Vision—Machine Learning Engineer",
        placeholder="e.g., Senior Data Scientist",
        help="Your current or desired job title"
    )

    job_summary = st.text_area(
        "Job Summary",
        value="4.5 years of experience as a Machine Learning Engineer with a PhD in Industrial Computer Science and expertise in generative AI. Proven track record in developing cutting-edge systems, including a fine-tuned diffusion model for image generation and a transformer-based OCR model that improved accuracy and performance. Skilled in building scalable LLM-RAG solutions and deploying AI models in production. Seeking a Machine Learning Engineer role to drive innovation and deliver impactful AI solutions.",
        placeholder="e.g., Senior Data Scientist with expertise in machine learning and data analysis",
        help="A brief summary of your professional background and key skills"
    )
    
    location = st.text_input(
        "Location",
        value="Lille, France",
        placeholder="e.g., San Francisco, CA",
        help="City and country/state"
    )

    email = st.text_input(
        "Email *",
        value="mohandash.youtube@gmail.com",
        placeholder="e.g., john.doe@example.com",
        help="Professional email address"
    )

with col2:
    phone = st.text_input(
        "Phone Number",
        value="+33-0750000000",
        placeholder="e.g., +1 (555) 123-4567",
        help="Include country code"
    )

    linkedin = st.text_input(
        "LinkedIn URL",
        value="https://www.linkedin.com/in/balyogi-mohan-dash/",
        placeholder="e.g., linkedin.com/in/johndoe",
        help="Your LinkedIn profile URL"
    )

    github = st.text_input(
        "GitHub URL",
        value="https://github.com/mohan696matlab",
        placeholder="e.g., github.com/johndoe",
        help="Your GitHub profile (optional)"
    )

    website = st.text_input(
        "Personal Website",
        value="https://www.youtube.com/@Mohankumardash",
        placeholder="e.g., johndoe.com",
        help="Portfolio or personal website"
    )

    google_scholar = st.text_input(
        "Google Scholar URL",
        value="https://scholar.google.com/citations?user=jzcIElIAAAAJ&hl=en",
        placeholder="e.g., scholar.google.com/citations?user=...",
        help="For academic profiles (optional)"
    )

st.markdown("---")

# =====================================================
#                   EDUCATION SECTION
# =====================================================
st.header("🎓 Education")

if "education_list" not in st.session_state:
        st.session_state.education_list = [
        {
            "institution": "University of Lille",
            "location": "Lille, France",
            "degree": "PhD in Computer Vision",
            "duration": "2021 - 2024",
            "lab_name": "CRIStAL - Computer Vision and Learning Lab",
            "lab_url": "https://www.cristal.univ-lille.fr/en/theses/dash-balyogi-mohan-803"
        },
        {
            "institution": "Indian Institute of Technology (IIT) Kharagpur",
            "location": "Kharagpur, India",
            "degree": "Master of Technology",
            "duration": "2019 - 2021",
            "lab_name": "",
            "lab_url": ""
        },
        # {
        #     "institution": "Veer Surendra Sai University of Technology (VSSUT) Burla",
        #     "location": "Burla, India",
        #     "degree": "Bachelor of Technology",
        #     "duration": "2015 - 2019",
        #     "lab_name": "",
        #     "lab_url": ""
        # },
    ]

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Add your academic qualifications, starting with the most recent.")
with col2:
    if st.button("➕ Add Education", use_container_width=True, key="add_edu_btn"):
        st.session_state.education_list.append({
            "institution": "",
            "location": "",
            "degree": "",
            "duration": "",
            "lab_name": "",
            "lab_url": ""
        })

if len(st.session_state.education_list) == 0:
    st.info("👆 Click 'Add Education' to add your first entry")

for idx, entry in enumerate(st.session_state.education_list):
    with st.container():
        st.markdown(f"""
        <div class="item-card">
            <h3>🎓 Education Entry {idx + 1}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            entry["institution"] = st.text_input(
                "Institution Name *", 
                entry["institution"], 
                key=f"inst_{idx}",
                placeholder="e.g., Stanford University"
            )
            entry["degree"] = st.text_input(
                "Degree *", 
                entry["degree"], 
                key=f"deg_{idx}",
                placeholder="e.g., Ph.D. in Computer Science"
            )
            entry["lab_name"] = st.text_input(
                "Lab/Research Group (optional)", 
                entry["lab_name"], 
                key=f"labn_{idx}",
                placeholder="e.g., AI Research Lab"
            )
        
        with col2:
            entry["location"] = st.text_input(
                "Location", 
                entry["location"], 
                key=f"loc_{idx}",
                placeholder="e.g., Stanford, CA"
            )
            entry["duration"] = st.text_input(
                "Duration *", 
                entry["duration"], 
                key=f"dur_{idx}",
                placeholder="e.g., 2018 - 2022"
            )
            entry["lab_url"] = st.text_input(
                "Lab URL (optional)", 
                entry["lab_url"], 
                key=f"labu_{idx}",
                placeholder="e.g., https://ailab.stanford.edu"
            )
        
        if st.button(f"🗑️ Delete Education Entry {idx + 1}", key=f"del_edu_{idx}"):
            st.session_state.education_list.pop(idx)
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")



# =====================================================
#                   WORK EXPERIENCE SECTION
# =====================================================
st.header("💼 Work Experience")

if "workex_list" not in st.session_state:
    st.session_state.workex_list = [
        {
            "company": "Buawei",
            "location": "Saint-André-lez-Lille, France",
            "role": "Research and Development Engineer",
            "duration": "Mar. 2024 – Present",
            "achievements": [
                {
                    "title": "Diffusion Model",
                    "achievement": "Developed end-to-end image generation pipeline using a fine-tuned diffusion model; implemented state-of-the-art image editing techniques with PyTorch & Hugging Face; optimized training using parameter-efficient fine-tuning; deployed via Git & Docker."
                },
                {
                    "title": "Transformer-Based OCR",
                    "achievement": "Fine-tuned transformer OCR on a custom dataset, improving F1-score by 8%; enhanced product recognition, delivering €200,000 additional revenue."
                },
                {
                    "title": "Visual Anomaly Detection",
                    "achievement": "Built real-time industrial quality control system using OpenCV & PyTorch; achieved 85% faster processing while maintaining accuracy."
                },
                {
                    "title": "Object Tracking",
                    "achievement": "Developed real-time object tracking and segmentation using SAM & OpenCV for aerospace contamination estimation; increased processing speed by 10% compared to manual methods."
                }
            ]
        },
        {
            "company": "University of Lille",
            "location": "Villeneuve d’Ascq, Lille, France",
            "role": "PhD Researcher",
            "duration": "Oct. 2021 – Mar. 2024",
            "achievements": [
                {
                    "title": "Fault Diagnosis using Machine Learning",
                    "achievement": "Published two Q1 journals, one Q2 journal, and two top-tier international conference papers as first author. Developed deep learning models for predicting the remaining useful life of industrial components, improving accuracy by 37%. Designed hybrid self-supervised fault diagnosis methods, reducing dependence on labeled data by 55%."
                },
                {
                    "title": "SNCF Track Condition Monitoring",
                    "achievement": "Led collaboration to create AI-based track monitoring system integrating physical knowledge, reducing false alarms, improving operational efficiency, and generating cost savings."
                }
            ]
        }
    ]



col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Add your professional experience, starting with your most recent position.")
with col2:
    if st.button("➕ Add Work Experience", use_container_width=True, key="add_work_btn"):
        st.session_state.workex_list.append({
            "company": "",
            "location": "",
            "role": "",
            "duration": "",
            "achievements": []
        })

if len(st.session_state.workex_list) == 0:
    st.info("👆 Click 'Add Work Experience' to add your first entry")

for idx, job in enumerate(st.session_state.workex_list):
    with st.container():
        st.markdown(f"""
        <div class="item-card">
            <h3>🏢 Experience {idx + 1}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            job["company"] = st.text_input(
                "Company Name *", 
                job["company"], 
                key=f"comp_{idx}",
                placeholder="e.g., Google LLC"
            )
            job["role"] = st.text_input(
                "Job Title/Role *", 
                job["role"], 
                key=f"comprole_{idx}",
                placeholder="e.g., Senior Machine Learning Engineer"
            )
        
        with col2:
            job["location"] = st.text_input(
                "Location", 
                job["location"], 
                key=f"comploc_{idx}",
                placeholder="e.g., Mountain View, CA"
            )
            job["duration"] = st.text_input(
                "Duration *", 
                job["duration"], 
                key=f"compdur_{idx}",
                placeholder="e.g., Jan 2020 - Present"
            )
        
        # Achievements subsection
        st.markdown("#### 🏆 Key Achievements")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("Add specific achievements, metrics, and impact from this role.")
        with col2:
            if st.button(f"➕ Add Achievement", key=f"add_ach_{idx}", use_container_width=True):
                job["achievements"].append({
                    "title": "",
                    "achievement": ""
                })
        
        if len(job["achievements"]) == 0:
            st.info("💡 Add achievements to highlight your impact in this role")
        
        for a_idx, ach in enumerate(job["achievements"]):
            st.markdown(f"**Achievement {a_idx + 1}**")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                ach["title"] = st.text_input(
                    "Short Title", 
                    ach["title"], 
                    key=f"achtitle_{idx}_{a_idx}",
                    placeholder="e.g., Model Optimization"
                )
            
            with col2:
                ach["achievement"] = st.text_area(
                    "Achievement Description", 
                    ach["achievement"], 
                    key=f"achdesc_{idx}_{a_idx}",
                    placeholder="e.g., Reduced inference time by 40% through model quantization"
                )
            
            if st.button(f"🗑️ Delete Achievement {a_idx + 1}", key=f"del_ach_{idx}_{a_idx}"):
                job["achievements"].pop(a_idx)
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(f"🗑️ Delete Work Experience {idx + 1}", key=f"del_work_{idx}"):
            st.session_state.workex_list.pop(idx)
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
#                   PROJECTS SECTION
# =====================================================
st.header("🚀 Projects")

if "projects_list" not in st.session_state:
    st.session_state.projects_list = [
        {
            "project_name": "Automatic Speech Recognition",
            "achievement": "Fine-tuned Whisper (Transformers) for Odia, a low-resource language, reducing character error rate from 85% to 25%. Demonstrates expertise in model fine-tuning, low-resource NLP, and speech recognition.",
            "project_url": "https://github.com/mohan696matlab/whisper-finetuning-youtube-serise/tree/main"
        },
        {
            "project_name": "RAG System",
            "achievement": "Designed a Retrieval-Augmented Generation system using LLAMA 3.2, LangChain, and ChromaDB for context-aware responses on the Bhagavad Gita. Developed FastAPI-based API for deployment, enhancing retrieval accuracy.",
            "project_url": "https://youtu.be/OscLQoDc9m4"
        },
        {
            "project_name": "Transformers from Scratch",
            "achievement": "Built a small language model from scratch in PyTorch, demonstrating self-supervised pretraining and supervised fine-tuning to create a basic chatbot.",
            "project_url": "https://youtu.be/Qxp3DpyzYgY"
        }
    ]


col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Showcase your key projects, side projects, or significant contributions.")
with col2:
    if st.button("➕ Add Project", use_container_width=True, key="add_project_btn"):
        st.session_state.projects_list.append({
            "project_name": "",
            "achievement": ""
        })

if len(st.session_state.projects_list) == 0:
    st.info("👆 Click 'Add Project' to add your first entry")

for idx, project in enumerate(st.session_state.projects_list):
    with st.container():
        st.markdown(f"""
        <div class="item-card">
            <h3>🔧 Project {idx + 1}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        project["project_name"] = st.text_input(
            "Project Name (optional)", 
            project["project_name"] if project["project_name"] else "", 
            key=f"proj_name_{idx}",
            placeholder="e.g., Real-time Analytics Dashboard"
        )
        
        project["achievement"] = st.text_area(
            "Key Details or Outcomes *", 
            project["achievement"], 
            key=f"proj_ach_{idx}",
            placeholder="e.g., Built a scalable dashboard using React and Python that processes 1M+ events daily, reducing reporting time by 60%",
            height=100
        )
        
        if st.button(f"🗑️ Delete Project {idx + 1}", key=f"del_proj_{idx}"):
            st.session_state.projects_list.pop(idx)
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
#                   SKILLS SECTION
# =====================================================
st.header("🛠️ Skills")

if "skills_list" not in st.session_state:
    st.session_state.skills_list = [
        {
            "skill_category": "Technical Skills",
            "skills": "Python, Machine Learning, Deep Learning, Generative AI, LLMs, Transformers, Diffusers, PyTorch, Hugging Face, Scikit-Learn, LangChain, ChromaDB, REST APIs, Docker, Git, Linux"
        },
        {
            "skill_category": "Transferable Skills",
            "skills": "Research, Team Collaboration, Analytics, Project Management, Communication"
        },
        {
            "skill_category": "Languages",
            "skills": "English (Bilingual), French (A2), Hindi, Odia"
        }
    ]


col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Organize your skills by category (e.g., Programming Languages, Tools, Soft Skills).")
with col2:
    if st.button("➕ Add Skill Category", use_container_width=True, key="add_skill_btn"):
        st.session_state.skills_list.append({
            "skill_category": "",
            "skills": ""
        })

if len(st.session_state.skills_list) == 0:
    st.info("👆 Click 'Add Skill Category' to add your first entry")

for idx, skill in enumerate(st.session_state.skills_list):
    with st.container():
        st.markdown(f"""
        <div class="item-card">
            <h3>⚡ Skill Category {idx + 1}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            skill["skill_category"] = st.text_input(
                "Category (optional)", 
                skill["skill_category"] if skill["skill_category"] else "", 
                key=f"skill_cat_{idx}",
                placeholder="e.g., Programming Languages"
            )
        
        with col2:
            skill["skills"] = st.text_input(
                "Skills *", 
                skill["skills"], 
                key=f"skill_items_{idx}",
                placeholder="e.g., Python, JavaScript, Java, C++",
                help="Enter skills separated by commas. Do not use brackets or quotes."
            )
        
        if st.button(f"🗑️ Delete Skill Category {idx + 1}", key=f"del_skill_{idx}"):
            st.session_state.skills_list.pop(idx)
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
#                   PUBLICATIONS SECTION
# =====================================================
st.header("📚 Publications")

if "publication_list" not in st.session_state:
    st.session_state.publication_list = [
        {
            "title": "Bond Graph-CNN based hybrid fault diagnosis with minimum labeled data",
            "venue": "Engineering Applications of Artificial Intelligence",
            "year": "2024",
            "doi": "https://doi.org/10.1016/j.engappai.2023.107734"
        },
        {
            "title": "Prior knowledge-infused Self-Supervised Learning and explainable AI for Fault Detection and Isolation in PEM electrolyzers",
            "venue": "Neurocomputing",
            "year": "2024",
            "doi": "https://doi.org/10.1016/j.neucom.2024.127871"
        },
        {
            "title": "Failure prognosis of the components with unlike degradation trends: A data-driven approach",
            "venue": "Proceedings of the Institution of Mechanical Engineers, Part O: Journal of Risk and Reliability",
            "year": "2023",
            "doi": "https://doi.org/10.1177/1748006X221119301"
        },
        {
            "title": "A comparison of model-based and machine learning techniques for fault diagnosis",
            "venue": "Proceedings of the 23rd International Middle East Power Systems Conference (MEPCON)",
            "year": "2022",
            "doi": "https://doi.org/10.1109/MEPCON55441.2022.10021712"
        },
        {
            "title": "FDI-X: An occlusion-based approach for improving the explainability of deep learning models in fault detection and isolation",
            "venue": "Proceedings of the 2023 International Conference on Control, Automation and Diagnosis (ICCAD)",
            "year": "2023",
            "doi": "https://doi.org/10.1109/ICCAD57653.2023.10152392"
        }
    ]


col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("List your published research papers, articles, or significant contributions.")
with col2:
    if st.button("➕ Add Publication", use_container_width=True, key="add_pub_btn"):
        st.session_state.publication_list.append({
            "title": "",
            "venue": "",
            "year": "",
            "doi": ""
        })

if len(st.session_state.publication_list) == 0:
    st.info("👆 Click 'Add Publication' to add your first entry")

for idx, pub in enumerate(st.session_state.publication_list):
    with st.container():
        st.markdown(f"""
        <div class="item-card">
            <h3>📄 Publication {idx + 1}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        pub["title"] = st.text_input(
            "Publication Title *", 
            pub["title"], 
            key=f"pubt_{idx}",
            placeholder="e.g., Deep Learning Approaches to Natural Language Processing"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pub["venue"] = st.text_input(
                "Venue/Conference *", 
                pub["venue"], 
                key=f"pubv_{idx}",
                placeholder="e.g., NeurIPS 2023"
            )
        
        with col2:
            pub["year"] = st.text_input(
                "Year *", 
                pub["year"], 
                key=f"puby_{idx}",
                placeholder="e.g., 2023"
            )
        
        with col3:
            pub["doi"] = st.text_input(
                "DOI/URL", 
                pub["doi"], 
                key=f"pubdoi_{idx}",
                placeholder="e.g., 10.1234/xyz"
            )
        
        if st.button(f"🗑️ Delete Publication {idx + 1}", key=f"del_pub_{idx}"):
            st.session_state.publication_list.pop(idx)
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
#                   JSON OUTPUT & DOWNLOAD
# =====================================================
st.header("💾 Export Your CV")

cv_data = {
    "name": name,
    "job_title": job_title,
    "summary": job_summary,
    "location": location,
    "email": email,
    "phone": phone,
    "linkedin": linkedin,
    "github": github,
    "website": website,
    "google_scholar": google_scholar,
    "education": st.session_state.education_list,
    "publications": st.session_state.publication_list,
    "work_experience": st.session_state.workex_list,
    "projects": st.session_state.projects_list,
    "skills": st.session_state.skills_list
}

# Validation check
required_fields = [name, job_title, email]
if all(required_fields):
    st.success("✅ All required fields completed! Ready to export.")
else:
    st.warning("⚠️ Please fill in all required fields marked with * before exporting.")

# Display JSON in expandable section
with st.expander("📄 Preview JSON Output"):
    st.json(cv_data)

# Download button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    json_string = json.dumps(cv_data, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 Download CV as JSON",
        file_name="cv_output.json",
        mime="application/json",
        data=json_string,
        use_container_width=True
    )
    if st.button("Preview PDF"):
        display_pdf(pdf_path)
    
    shutil.rmtree('cv_cache', ignore_errors=True, onerror=None)
    os.makedirs("cv_cache", exist_ok=True)  # Ensure cache directory exists
    generate_latex_cv(json_data=cv_data, 
                      output_tex_file="cv_cache/cv_output.tex", 
                      output_pdf_dir="cv_cache")
    st.session_state.last_cv_data = cv_data  # update memory
    st.success("CV updated!")

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem 0; border-top: 1px solid #e5e7eb; margin-top: 2rem;'>
    <p>💡 <strong>Tip:</strong> Save your progress regularly by downloading the JSON file.</p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem;'>Built with Streamlit | © 2024 CV Builder</p>
</div>
""", unsafe_allow_html=True)