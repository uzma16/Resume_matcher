

# import streamlit as st
# import requests

# def main():
#     st.title("Resume Matching App")
#     st.write("Upload your Resume and Job Description")

#     # Upload Resume
#     resume = st.file_uploader("Upload Resume", type=['pdf', 'docx'])

#     # Upload Job Description
#     job_description = st.file_uploader("Upload Job Description", type=['pdf', 'docx'])

#     # Submit Button
#     if st.button("Submit"):
#         if resume and job_description:
#             response = upload_files(resume, job_description)
#             if response.status_code == 201:
#                 st.success("Files uploaded successfully!")
#                 # Display extracted skills and narrative if available
#                 response_data = response.json()
#                 for item in response_data:
#                     if 'data' in item:
#                         if 'skills' in item['data']:
#                             st.markdown("**You must have these skills for this job, According to the JD that you provided:**")
#                             show_skills_in_box(item['data']['skills'])
#                         if 'narrative' in item['data']:
#                             st.markdown("**Script for 'Tell me about yourself', According to the given JD & Resume**")
#                             # with st.expander("Skills", expanded=True):
#                             st.write(item['data']['narrative'])
#             else:
#                 st.error("Failed to upload files")
#         else:
#             st.error("Please upload both Resume and Job Description.")

# def upload_files(resume, job_description):
#     url = 'http://localhost:8000/api/upload/'
#     files = {'resume': (resume.name, resume.getvalue(), resume.type),
#              'job_description': (job_description.name, job_description.getvalue(), job_description.type)}
#     response = requests.post(url, files=files)
#     return response

# def show_skills_in_box(skills):
#     # Display skills inside a box
#     with st.expander("Skills", expanded=True):
#         for skill in skills:
#             st.write(f"- {skill}")

# # def show_skills_in_box(skills):
# #     # Display skills inside a box
# #     with st.expander("Skills", expanded=True):
# #         for i in range(0, len(skills), 2):  # Display two skills per row
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if i < len(skills):
# #                     st.write(f"- {skills[i]}")
# #             with col2:
# #                 if i + 1 < len(skills):
# #                     st.write(f"- {skills[i + 1]}")

# if __name__ == "__main__":
#     main()


import streamlit as st
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    st.title("Resume Matching App")
    st.write("Upload your Resume and Job Description")

    # Upload Resume
    resume = st.file_uploader("Upload Resume", type=['pdf', 'docx'])

    # Upload Job Description
    job_description = st.file_uploader("Upload Job Description", type=['pdf', 'docx'])

    # Submit Button
    if st.button("Submit"):
        if resume and job_description:
            response = upload_files(resume, job_description)
            if response.status_code == 201:
                st.success("Files uploaded successfully!")
                # Display extracted skills, narrative, and donut charts if available
                response_data = response.json()
                for item in response_data:
                    if 'data' in item:
                        if 'skills' in item['data']:
                            st.markdown("**You must have these skills for this job, According to the JD that you provided:**")
                            show_skills_in_box(item['data']['skills'])
                        if 'narrative' in item['data']:
                            st.markdown("**Unveiling the Ultimate 'Tell Me About Yourself' Script: A Fusion of Your Resume and Job Description to Ace Any Interview!**")
                            st.write(item['data']['narrative'])
                        if 'Skills' in item['data']:
                            show_donut_charts(item['data']['Skills'], item['data']['Languages'], item['data']['Experience'])
    
                        # if 'Skills' in item['data']:
                        #     show_donut_chart("Skills", item['data']['Skills'])
                        # if 'Languages' in item['data']:
                        #     show_donut_chart("Languages", item['data']['Languages'])
                        # if 'Experience' in item['data']:
                        #     show_donut_chart("Experience", item['data']['Experience'])
            else:
                st.error("Failed to upload files")
        else:
            st.error("Please upload both Resume and Job Description.")

def upload_files(resume, job_description):
    url = 'http://localhost:8000/api/upload/'
    files = {'resume': (resume.name, resume.getvalue(), resume.type),
             'job_description': (job_description.name, job_description.getvalue(), job_description.type)}
    response = requests.post(url, files=files)
    return response

def show_skills_in_box(skills):
    # Display skills inside a box
    with st.expander("Skills", expanded=True):
        for skill in skills:
            st.write(f"- {skill}")

# def show_donut_chart(title, data):
#     total_value = data.get('Total', 0)
#     remaining_value = 100 - total_value
    
#     # Create figure
#     fig = go.Figure(data=[go.Pie(labels=['Total', 'Remaining'], 
#                                   values=[total_value, remaining_value], 
#                                   hole=.3,
#                                   marker=dict(colors=['green', 'red']))])
#     fig.update_layout(title=f"{title} Total", title_x=0.5)
    
#     # Display figure
#     st.write(fig)
def show_donut_charts(skills_data, languages_data, experience_data):
    # Create figure for donut charts
    fig = go.Figure()

    # Add donut chart for Skills
    fig.add_trace(go.Pie(labels=['Skills Match', 'Remaining'], 
                         values=[skills_data.get('Skills Match Percentage', 0), 100 - skills_data.get('Total', 0)], 
                         hole=0.6, 
                         marker=dict(colors=['#00FF00', '#00693E']),
                         domain=dict(x=[0, 0.3])))

    # Add donut chart for Languages
    fig.add_trace(go.Pie(labels=['Language Match', 'Remaining'], 
                         values=[languages_data.get('Languages Match Percentage', 0), 100 - languages_data.get('Total', 0)], 
                         hole=0.6, 
                         marker=dict(colors=['#ADD8E6', '#abd4f8']),
                         domain=dict(x=[0.35, 0.65])))

    # Add donut chart for Experience
    fig.add_trace(go.Pie(labels=['Experience Match', 'Remaining'], 
                         values=[experience_data.get('Experience Match Percentage', 0), 100 - experience_data.get('Total', 0)], 
                         hole=0.6, 
                         marker=dict(colors=['#f0a1a0', '#e97782']),
                         domain=dict(x=[0.7, 1])))

    # Update layout
    fig.update_layout(height=400, width=800, title_text="Matching Charts")

    # Display figure
    st.plotly_chart(fig)
            

if __name__ == "__main__":
    main()




#------------------------------Working---------------------------------------------#
# import streamlit as st
# import requests
# import matplotlib.pyplot as plt

# def main():
#     st.title("Resume Matching App")
#     st.write("Upload your Resume and Job Description")

#     # Upload Resume
#     resume = st.file_uploader("Upload Resume", type=['pdf', 'docx'])

#     # Upload Job Description
#     job_description = st.file_uploader("Upload Job Description", type=['pdf', 'docx'])

#     # Submit Button
#     if st.button("Submit"):
#         if resume and job_description:
#             response = upload_files(resume, job_description)
#             if response.status_code == 201:
#                 st.success("Files uploaded successfully!")
#                 # Display extracted skills and narrative if available
#                 response_data = response.json()
#                 for item in response_data:
#                     if 'data' in item:
#                         if 'skills' in item['data']:
#                             st.markdown("**You must have these skills for this job, According to the JD that you provided:**")
#                             show_skills_in_box(item['data']['skills'])
#                         if 'narrative' in item['data']:
#                             st.markdown("**Script for 'Tell me about yourself', According to the given JD & Resume**")
#                             # with st.expander("Skills", expanded=True):
#                             st.write(item['data']['narrative'])
#                         if 'match_percentage' in item['data']:
#                             show_match_percentage(item['data']['match_percentage'])
#             else:
#                 st.error("Failed to upload files")
#         else:
#             st.error("Please upload both Resume and Job Description.")

# def upload_files(resume, job_description):
#     url = 'http://localhost:8000/api/upload/'
#     files = {'resume': (resume.name, resume.getvalue(), resume.type),
#              'job_description': (job_description.name, job_description.getvalue(), job_description.type)}
#     response = requests.post(url, files=files)
#     return response

# def show_skills_in_box(skills):
#     # Display skills inside a box
#     with st.expander("Skills", expanded=True):
#         for skill in skills:
#             st.write(f"- {skill}")

# # def show_match_percentage(percentage):
# #     # Convert percentage to a fraction between 0 and 1
# #     fraction = percentage / 100
# #     print(fraction)
# #     # Display match percentage using a progress bar
# #     st.write("Match Percentage:")
# #     st.progress(fraction)
# def show_match_percentage(percentage):
#     # Convert percentage to a fraction between 0 and 1
#     fraction = percentage / 100
#     # Calculate remaining percentage
#     remaining_percentage = 1 - fraction

#     # Plot the donut chart
#     fig, ax = plt.subplots()
#     ax.pie([fraction, remaining_percentage], colors=['green', 'red'], startangle=90, counterclock=False, wedgeprops=dict(width=0.3))

#     # Draw a circle in the center to make it a donut chart
#     centre_circle = plt.Circle((0,0),0.2,fc='white')
#     fig = plt.gcf()
#     fig.gca().add_artist(centre_circle)

#     # Equal aspect ratio ensures that pie is drawn as a circle.
#     ax.axis('equal')  

#     # Display the plot
#     st.pyplot(fig)

# if __name__ == "__main__":
#     main()
#--------------------------------------------------------------Working-------------------------------------------------------------

