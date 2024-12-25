import streamlit as st
import info
import pandas as pd

#About Me
def about_me_section():
    st.header("About Me")
    st.image(info.profile_picture, width = 200)
    st.write(info.about_me)
    st.write("---")
about_me_section()

#Sidebar Links
def links_section():
    st.sidebar.header("Links")
    st.sidebar.text("Connect with me on LinkedIn")
    linkedin_link= f'<a href="{info.my_linkedin_url}"><img src="{info.linkedin_image_url}" alt="Linkedin" width = "75" height ="75"></a>'
    st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
    st.sidebar.text("Checkout my work")
    github_link= f'<a href="{info.my_github_url}"><img src="{info.github_image_url}" alt="github" width = "65" height ="65"></a>'
    st.sidebar.markdown(github_link, unsafe_allow_html=True)
    st.sidebar.text("Or email me \n@mariomarioapi277@gmail.com!")
    email_link= f'<a href="{info.my_email_address}"><img src="{info.email_image_url}" alt="Email" width = "75" height ="75"></a>'
    st.sidebar.markdown(email_link, unsafe_allow_html=True)
links_section()

#Education
def education_section(education_data, course_data):
    st.header("Education")
    st.subheader(f"**{education_data['Institution']}**")
    st.write(f"Degree: {education_data['Degree']}")
    st.write(f"Graduation Date: {education_data['Graduation Date']}")
    st.write(f"GPA: {education_data['GPA']}")
    st.write("Relevant Coursework:")
    coursework = pd.DataFrame(course_data)
    st.dataframe(coursework, column_config={
        "code": "Course Code",
        "names": "Course Names",
        "semester_taken": "Semester Taken",
        "skills": "What I Learned"},
        hide_index=True
        )
    st.write("---")

education_section(info.education_data, info.course_data)

#Professional Experience

def experience_section(experience_data):
    st.header("Professional Experience")
    for job_title, (job_description, image) in experience_data.items():
        expander = st.expander(f"{job_title}")
        expander.image(image, width=250)
        for bullet in job_description:
            expander.write(bullet)
    st.write("---")
experience_section(info.experience_data)

#Projects

def project_section(projects_data):
    st.header("Projects")
    for project_name, project_description in projects_data.items():
        expander = st.expander(f"{project_name}")
        expander.write(project_description)
    st.write("---")
project_section(info.projects_data)

#Skills

def skills_section(gaming_data, spoken_data):
    st.header("Skills")
    st.subheader("Gaming Abilities")
    for skill, percentage in gaming_data.items():
        st.write(f"{skill} {info.gaming_icons.get(skill, )}")
        st.progress(percentage)
    st.subheader("Spoken Languages")
    for spoken, proficiency in spoken_data.items():
        st.write(f"{spoken} {info.spoken_icons.get(spoken, )}: {proficiency}")

    st.write("---")
skills_section(info.gaming_data, info.spoken_data)

#Activities

def activities_section(leadership_data, activity_data):
    st.header("Activities")
    tab1, tab2 = st.tabs(["Leadership", "Community Service"])
    with tab1:
        st.subheader("Leadership")
        for title, (details, image) in leadership_data.items():
            expander = st.expander(f"{title}")
            expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
    with tab2:
        st.subheader("Community Service")
        for title, details in activity_data.items():
            expander = st.expander(f"{title}")
            for bullet in details:
                expander.write(bullet)

    st.write("---")

activities_section(info.leadership_data, info.activity_data)

