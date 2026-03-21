from app.database import SessionLocal
from app.models.models import Project, SkillGroup, Certification, AdminUser
from app.core.security import hash_password


def seed_data():
    db = SessionLocal()
    try:
        # Only seed if tables are empty
        if db.query(Project).count() > 0:
            return

        # ── PROJECTS ────────────────────────────────────────────
        projects = [
            Project(
                num="001", title="Early Detection of Cancer Using AI",
                org="St. Mary's Group of Institutions", date="Feb 2026",
                description="AI-based predictive system to detect early signs of cancer from medical data using ML algorithms and statistical analysis. Performed data preprocessing, feature selection, and model training to improve prediction accuracy and reduce false negatives. Evaluated model performance using accuracy, precision, recall, and ROC curves.",
                stack=["Python", "Scikit-learn", "Pandas", "ROC Curves", "Feature Engineering"],
                color="#f97316", is_featured=True, order=1,
            ),
            Project(
                num="002", title="OCR System",
                org="St. Mary's Group of Institutions", date="Oct 2025",
                description="Optical Character Recognition system to extract and digitize text from images and scanned documents using image preprocessing and recognition techniques. Implemented automated text extraction and structured output generation, reducing manual data entry effort.",
                stack=["Python", "Image Processing", "NLTK", "TensorFlow", "OpenCV"],
                color="#22d3ee", is_featured=True, order=2,
            ),
            Project(
                num="003", title="Sales Dashboard — Power BI",
                org="St. Mary's Group of Institutions", date="Apr 2024",
                description="Interactive Sales Dashboard in Power BI integrating data from CRM, sales databases, and financial reports. Implemented ETL processes using Power Query and built data models with DAX for KPIs. Automated report generation reduced manual effort by 70%.",
                stack=["Power BI", "DAX", "Power Query", "ETL", "Data Modeling"],
                color="#a78bfa", is_featured=True, order=3,
            ),
            Project(
                num="004", title="Online Registration Form",
                org="St. Mary's Group of Institutions", date="Jul – Sep 2023",
                description="Web-based registration form using HTML, CSS, JavaScript, and Python (Flask) to collect and validate user information. Implemented form validation, input sanitization, and database connectivity (MySQL) to securely store user records.",
                stack=["HTML", "CSS", "JavaScript", "Flask", "MySQL"],
                color="#34d399", is_featured=True, order=4,
            ),
        ]
        db.add_all(projects)

        # ── SKILLS ──────────────────────────────────────────────
        skill_groups = [
            SkillGroup(group="AI & Machine Learning", color="#f97316", order=1,
                tags=["Model Development", "Supervised Learning", "Unsupervised Learning", "Feature Engineering", "Data Preprocessing", "Model Evaluation", "Hyperparameter Tuning", "Bias–Variance Analysis"]),
            SkillGroup(group="Data Analysis & Visualization", color="#22d3ee", order=2,
                tags=["Data Cleaning", "EDA", "Statistical Analysis", "Dashboarding", "Insight Generation", "Data Transformation"]),
            SkillGroup(group="Languages & Libraries", color="#a78bfa", order=3,
                tags=["Python", "Java", "R", "JavaScript", "TensorFlow", "Scikit-learn", "NLTK", "NumPy", "Pandas", "Matplotlib", "Seaborn", "Streamlit", "Flask"]),
            SkillGroup(group="Tools & Platforms", color="#34d399", order=4,
                tags=["Jupyter Notebook", "Google Colab", "VS Code", "Git", "Docker", "Kaggle", "n8n", "Linux", "SQL", "MySQL", "Power BI"]),
            SkillGroup(group="Core CS Concepts", color="#f472b6", order=5,
                tags=["Data Structures & Algorithms", "OOP", "Operating Systems", "Computer Networks", "DBMS"]),
            SkillGroup(group="Deployment & Practical", color="#facc15", order=6,
                tags=["Model Integration", "API Development", "Prototype Deployment", "Testing & Validation"]),
        ]
        db.add_all(skill_groups)

        # ── CERTIFICATIONS ───────────────────────────────────────
        certs = [
            Certification(name="Python Essentials", org="CISCO", date="Dec 2024", order=1),
            Certification(name="Artificial Intelligence", org="Infosys Springboard", date="Jun 2025", order=2),
            Certification(name="Introduction to Artificial Intelligence", org="Infosys Springboard", date="Jun 2025", order=3),
            Certification(name="Agile Project Management", org="HP", date="Nov 2024", order=4),
        ]
        db.add_all(certs)

        # ── ADMIN USER ───────────────────────────────────────────
        admin = AdminUser(username="mahesh", hashed_password=hash_password("admin123"))
        db.add(admin)

        db.commit()
        print("✅ Database seeded with Mahesh's portfolio data.")
    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
    finally:
        db.close()
