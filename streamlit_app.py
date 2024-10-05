import streamlit as st
import anthropic
import json
from datetime import datetime
import typst
import PyPDF2
from io import BytesIO
from fpdf import FPDF
import logging


# Set page configuration
st.set_page_config(
    page_title="Tailored Resume Generator",
    layout="wide",
)

# Title of the app
st.title("Tailored Resume Generator")

# Sidebar for API Key (optional if using secrets)
# You can choose to use Streamlit Secrets instead for better security
# api_key = st.sidebar.text_input("Anthropic API Key", type="password")

# Alternatively, retrieve API key from secrets
api_key = st.secrets["anthropic"]["api_key"]

# File uploader for Original Resume (optional)
# If you want to allow users to upload their resume instead of using a predefined one
# uploaded_resume = st.file_uploader("Upload Your Resume (Text)", type=["txt", "pdf"])

# Text area for Original Resume
st.header("Original Resume")
original_resume = st.text_area("Enter your original resume content here:", height=400, value="""= Peerapat Chiaprasert (Chin)
peerapat.chiaprasert@gmail.com |
#link("https://linkedin.com/in/chpeerapat")[linkedin.com/in/chpeerapat] |
(+66)86-624-6630 | Bangkok, Thailand]
== PROFILE SUMMARY
#chiline()
*Strategic and results-driven leader with over 8 years of experience in launching and scaling new ventures within tech startups and management consulting. Expertise in developing and implementing growth strategies, optimizing operational efficiencies, and leading cross-functional teams to achieve business objectives.*
- Propelled GrabFood to become Thailand's top food delivery service within 8 months by implementing strategic go-to-market initiatives and setting up all business functions required.
- Founded GrabKitchen as Thailand's largest cloud kitchen network, generating over 400M THB in annual GMV by leveraging data-driven growth strategies, securing key partnerships, and developing scalable business models.
- Expanded TiffinLabs' delivery-centric restaurant brands to 100 storefronts, resulting in a 20% monthly increase in GMV and a 15% reduction in COGS through strategic operational enhancements and partnership negotiations.
== AREAS OF EXPERTISE
#chiline()
#columns(3)[
  #align(center)[
    Business Innovation\
    Operational Strategy\
    Account Management\
    Data-driven Analysis
  ]
#colbreak()
  #align(center)[
    Strategic Planning\
    Cross-functional Collaboration\
    P&L Management\
    Team Leadership
  ]
#colbreak()
  #align(center)[
    Business Development\
    Commercial Strategy\
    Strategic Partnerships\
    Feasibility Study
  ]
]
== WORK EXPERIENCE
#chiline()
*TiffinLabs*#h(1fr) Mar 2022 -- Oct 2023 \\
*Country General Manager*
- Expanded TiffinLabs' delivery-centric brand to 100 storefronts in Thailand. Led and developed the entire business team, overseeing marketing, business development, and operations. Streamlined processes for efficient growth and market penetration.
- Developed product value propositions for 7 delivery-focused food brands. Defined brand roadmaps ensuring product-market fit and established processes to capture evolving trends. Continuously refined offerings based on consumer feedback.
- Boosted GMV by 20% monthly through strategic marketing collaborations with delivery platforms. Maximized NPD sales by aligning promotional efforts and implementing regular product enhancements through agile methodology.
- Achieved 15% COGS reduction by initiating fulfillment partnerships with distributors. Negotiated favorable terms to meet target pricing and quality standards. Improved sourcing processes, resulting in faster procurement and increased efficiency.

*Grab*#h(1fr) Jun 2017 -- Feb 2022 \\
*Head, GrabKitchen* (2019-2022)
- Established Thailand's largest cloud kitchen network, GrabKitchen, developing an asset-lite model. Secured partnership with top F&B company CRG, creating a scalable, profitable business model for long-term growth.
- Grew GMV by average 25% per month and achieved 4x ROI through strategic marketing campaigns. Managed thematic promotions, partnerships, and Joint Business Plans to drive customer engagement and increase platform usage.
- Created a data-driven model for selecting profitable expansion locations. Utilized past performance data and location-specific demand trends to calculate individual kitchen profitability and determine accurate payback periods.
- Managed a diverse portfolio exceeding 400 million THB in annual GMV. Oversaw 120+ F&B accounts, including street vendors, local chains, QSRs, and strategic partners, ensuring optimal selections across segments to maximize growth
*Operations Manager, GrabFood | Special Project Lead, GrabBike & GrabExpress* (2017-2019)
- Propelled GrabFood to market leadership within 8 months through strategic initiatives. Established and optimized key functions including fleet management, business development, revenue collection, and customer services.
- Developed e-commerce strategies for leading F&B brands. Designed tailored solutions to launch and grow online channel for major brands such as MK, Starbucks, and CRG, driving online growth and enhancing market competitiveness
- Built and mentored high-performing teams across various functions and locations.  Oversaw 100+ staff members, including 7 direct reports, fostering a culture of excellence and continuous improvement throughout the organization.

*Ipsos Business Consulting* #h(1fr) Jul 2016 -- May 2017 \\
*Associate Consultant*
- Developed e-payment business model and identified strategic partners for successful launch. Utilized insightful market data to shortlist potential collaborators, ensuring a strong foundation for the new venture.
- Designed go-to-market strategy for Thai financial institution's e-commerce launch. Conducted comprehensive market research and analysis to inform strategic decisions and optimize market entry approach.
*EY (Ernst & Young)* #h(1fr) Feb 2015 -- Jun 2016 \\
*Consultant*
- Created costing model to pinpoint service costs and address profitability issues for Ministry of Public Health hospitals nationwide. Analyzed data to identify root causes and areas for financial improvement and efficiency gains.
- Enhanced efficiency for listed manufacturing company through business process improvement. Recommended new flow charts, SOPs, and integrated ERP systems to streamline operations and boost overall productivity.
== EDUCATION
#chiline()
*Thammasat University* #h(1fr) Jun 2011 -- Dec 2014 \\
Bachelor of Accounting (International Program)
""")

# Text area for Job Description
st.header("Job Title")
role = st.text_area("Enter the job title here:", height=200, value="""head of operations"""),
st.header("Job Description") 
job_description = st.text_area("Enter the job description here:", height=400, value="""About the job
Job Description:

Lead the end-to-end business development process for new ventures, including market research, feasibility studies, and competitive analysis.
Develop and implement strategic business plans that ensure the successful launch, growth, and profitability of new businesses (laundry, restaurants, market business, and more).
Oversee day-to-day operations for the new businesses, ensuring operational efficiency, cost-effectiveness, and high-quality service delivery.
Identify new market opportunities and trends to continuously innovate and expand the company's business portfolio.
Build and maintain strong relationships with external partners, vendors, and industry experts to drive collaboration and growth.
Manage financial performance by setting budgets, forecasts, and financial models to ensure profitability and scalability.
Collaborate with cross-functional teams (marketing, operations, finance, etc.) to ensure smooth business integration and alignment with corporate goals.
Monitor key performance indicators (KPIs) and make data-driven decisions to optimize business performance.
Provide leadership and mentorship to team members to foster a culture of innovation, collaboration, and continuous improvement.

Qualifications:

Bachelor's degree in Business Administration, Management, or a related field (Master's degree preferred).
Minimum of 8-10 years of experience in business development, with a strong focus on launching and managing new businesses.
Proven experience in both operational and strategic roles, ideally in retail, food and beverage, services, or market-related industries.
Strong business acumen with the ability to analyze market trends, financial data, and competitive landscapes.
Excellent leadership and team management skills, with a proven track record of leading cross-functional teams.
Strong interpersonal and communication skills, both verbal and written, with the ability to build strong relationships with stakeholders at all levels.
Highly adaptable and capable of handling multiple projects simultaneously in a fast-paced environment.
Strong problem-solving skills and the ability to make sound decisions under pressure.""")

# Button to generate tailored resume
if st.button("Generate Tailored Resume"):
    with st.spinner("Generating tailored resume..."):
            client = anthropic.Anthropic(
                api_key=api_key
            ) 
            message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                         "type": "text",
                         "text":  f"""You are an AI assistant tasked with analyzing a resume and a job description to create customized content for a job application. Your goal is to provide truthful and relevant information based on the given resume while tailoring it to the specific job requirements.

                                    First, carefully read and analyze the following documents:

                                    <resume>
                                    {original_resume}
                                    </resume>

                                    <job_description>
                                    {job_description}
                                    </job_description>

                                    After analyzing both documents, you will create customized content in three parts:

                                    1. Profile Summary:
                                    Create a 2-3 sentence statement that explains the candidate's years of experience, industry expertise, and highlights the most relevant skills for the job. Ensure that all information is truthful and can be inferred from the original resume. Tailor this summary to match the requirements in the job description.

                                    2. Key Achievements:
                                    List 3 bullet points, each showing an achievement from past experience that provides solid evidence for the profile summary. These achievements should be directly taken or reasonably inferred from the resume and should be relevant to the job description.

                                    3. Areas of Expertise:
                                    Provide a list of 12 skills that are most relevant to the job description. These skills should be mentioned in or inferred from the resume and align closely with the requirements listed in the job description.

                                    Present your analysis in JSON format with the following schema:
                                    {{
                                    "profile_summary": {{
                                        "type": "string",
                                        "description": "A brief summary of the individual's professional background and skills."
                                    }},
                                    "key_achievements": {{
                                        "type": "array",
                                        "description": "A list of key achievements highlighting significant accomplishments.",
                                        "items": {{
                                        "type": "string",
                                        "description": "A single key achievement."
                                        }},
                                        "minItems": 1,
                                        "uniqueItems": true
                                    }},
                                    "areas_of_expertise": {{
                                        "type": "array",
                                        "description": "A list of areas where the individual has specialized expertise.",
                                        "items": {{
                                        "type": "string",
                                        "description": "A single area of expertise."
                                        }},
                                        "minItems": 1,
                                        "uniqueItems": true
                                    }}
                                    }}

                                    Remember to provide only truthful information that can be referenced from or inferred from the original resume. Ensure that all content is tailored to match the requirements specified in the job description. """
                                    }
                                ]
                            }
                        ]
                    )
            print(message.content)
            # Extract the content
            tailored_content = (message.content)  # Extract content

# Check if tailored_content is a list and get the first element
            if isinstance(tailored_content, list) and len(tailored_content) > 0:
                tailored_content = tailored_content[0]  # Get the first element which should be TextBlock

# Check if tailored_content is a TextBlock object and extract its text attribute
            if hasattr(tailored_content, 'text'):
                json_string = tailored_content.text  # Extract the actual JSON string

    # Ensure json_string is a string before attempting to parse it
            if isinstance(json_string, str):
        # Parse the JSON content
                try:
                    data = json.loads(json_string)
                    print("JSON data successfully parsed.")
                except json.JSONDecodeError as e:
                    print("Failed to parse JSON:", e)
                    data = None
                else:
                    print("Error: tailored_content does not contain valid JSON data.")

# Verify the parsed data (Optional)
if data:
    print("\n--- Profile Summary ---")
    print(data['profile_summary'])

    # print("\n--- Key Achievements ---")
    # for idx, achievement in enumerate(data['key_achievements'], 1):
    #     print(f"{idx}. {achievement}")

    print("\n--- Areas of Expertise ---")
    for idx, skill in enumerate(data['areas_of_expertise'], 1):
        print(f"{idx}. {skill}") 

            # Extract data
        profile_summary = data.get('profile_summary', "") 
        key_achievements = data.get('key_achievements', []) 
        areas_of_expertise = data.get('areas_of_expertise', []) 

            # Ensure exactly 3 key achievements
        if len(key_achievements) < 3:
                key_achievements += [""] * (3 - len(key_achievements))
        elif len(key_achievements) > 3:
                key_achievements = key_achievements[:3]

            # Ensure exactly 12 areas of expertise
        if len(areas_of_expertise) < 12: 
                areas_of_expertise += [""] * (12 - len(areas_of_expertise)) 
        elif len(areas_of_expertise) > 12: 
                areas_of_expertise = areas_of_expertise[:12]
                st.json(data)
            # Define the Typst template with placeholders 
    template = f"""#set text(font: "inter",size: 8.5pt, hyphenate: true, ligatures: false, weight: "regular") 
#set page(margin: (x: 0.9cm, y: 0.9cm))
#set par(justify: true, leading: 0.7em,linebreaks: "optimized")
#set block(below: 1.1em)
#set list(tight: true, spacing: auto)
#let chiline() = {{v(-3pt); line(length: 100%); v(-5pt)}}
#set list(marker: [•])
#show heading.where(level: 1): set text(fill: blue,font: "inter")
#show heading.where(level: 2): set text(fill: blue,font: "inter")
#show heading.where(level: 3): set text(fill: blue,font: "inter")
#align(center)[
= Peerapat Chiaprasert (Chin)
peerapat.chiaprasert@gmail.com |
#link("https://linkedin.com/in/chpeerapat")[linkedin.com/in/chpeerapat] |
(+66)86-624-6630 | Bangkok, Thailand]
== PROFILE SUMMARY
#chiline()
*{profile_summary}*
- {key_achievements[0]}
- {key_achievements[1]}
- {key_achievements[2]}
== AREAS OF EXPERTISE
#chiline()
#columns(3)[
  #align(center)[
    {areas_of_expertise[0]}\\
    {areas_of_expertise[1]}\\
    {areas_of_expertise[2]}\\
    {areas_of_expertise[3]}
  ]
#colbreak()
  #align(center)[
    {areas_of_expertise[4]}\\
    {areas_of_expertise[5]}\\
    {areas_of_expertise[6]}\\
    {areas_of_expertise[7]}
  ]
#colbreak()
  #align(center) [
    {areas_of_expertise[8]}\\
    {areas_of_expertise[9]}\\
    {areas_of_expertise[10]}\\
    {areas_of_expertise[11]}
  ]
]
== WORK EXPERIENCE
#chiline()
*TiffinLabs*#h(1fr) Mar 2022 -- Oct 2023 \\
*Country General Manager*
- Expanded TiffinLabs' delivery-centric brand to 100 storefronts in Thailand. Led and developed the entire business team, overseeing marketing, business development, and operations. Streamlined processes for efficient growth and market penetration.
- Developed product value propositions for 7 delivery-focused food brands. Defined brand roadmaps ensuring product-market fit and established processes to capture evolving trends. Continuously refined offerings based on consumer feedback.
- Boosted GMV by 20% monthly through strategic marketing collaborations with delivery platforms. Maximized NPD sales by aligning promotional efforts and implementing regular product enhancements through agile methodology.
- Achieved 15% COGS reduction by initiating fulfillment partnerships with distributors. Negotiated favorable terms to meet target pricing and quality standards. Improved sourcing processes, resulting in faster procurement and increased efficiency.
*Grab*#h(1fr) Jun 2017 -- Feb 2022 \\
*Head, GrabKitchen* (2019-2022)
- Established Thailand's largest cloud kitchen network, GrabKitchen, developing an asset-lite model. Secured partnership with top F&B company CRG, creating a scalable, profitable business model for long-term growth.
- Grew GMV by average 20% per month and achieved 4x ROI through strategic marketing campaigns. Managed thematic promotions, partnerships, and Joint Business Plans to drive customer acquisition and retention .
- Created a data-driven model for selecting profitable expansion locations. Utilized past performance data and location-specific demand trends to calculate individual kitchen profitability and determine accurate payback periods.
- Managed a diverse portfolio exceeding 400 million THB in annual GMV. Oversaw 120+ F&B accounts, including street vendors, local chains, QSRs, and strategic partners, ensuring optimal selections across segments to maximize growth
*Operations Manager, GrabFood | Special Project Lead, GrabBike & GrabExpress* (2017-2019)
- Propelled GrabFood to market leadership within 8 months through strategic initiatives. Established and optimized key functions including fleet management, business development, revenue collection, and customer services.
- Developed e-commerce strategies for leading F&B brands. Designed tailored solutions to launch and grow online channel for major brands such as MK, Starbucks, and CRG, driving online growth and enhancing market competitiveness
- Built and mentored high-performing teams across various functions and locations.  Oversaw 100+ staff members, including 7 direct reports, fostering a culture of excellence and continuous improvement throughout the organization.
*Ipsos Business Consulting* #h(1fr) Jul 2016 -- May 2017 \\
*Associate Consultant*
- Developed e-payment business model and identified strategic partners for successful launch. Utilized insightful market data to shortlist potential collaborators, ensuring a strong foundation for the new venture.
- Designed go-to-market strategy for Thai financial institution's e-commerce launch. Conducted comprehensive market research and analysis to inform strategic decisions and optimize market entry approach.
*EY (Ernst & Young)* #h(1fr) Feb 2015 -- Jun 2016 \\
*Consultant*
- Created costing model to pinpoint service costs and address profitability issues for Ministry of Public Health hospitals nationwide. Analyzed data to identify root causes and areas for financial improvement and efficiency gains.
- Enhanced efficiency for listed manufacturing company through business process improvement. Recommended new flow charts, SOPs, and integrated ERP systems to streamline operations and boost overall productivity.
== EDUCATION
#chiline()
            *Thammasat University* #h(1fr) Jun 2011 -- Dec 2014 \\
            Bachelor of Accounting (International Program)
            """
            # Save the template to a temporary .typ file
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename_typ = f"Tailored_Resume_{current_date}_{role}.typ"
    with open(filename_typ, "w", encoding="utf-8") as file:
        file.write(template)

            # Compile Typst to PDF
    output_pdf = f"Tailored_Resume_{current_date}_{role}.pdf"
    try:
        # Assuming default fonts; adjust 'font_paths' if custom fonts are needed
        typst.compile(filename_typ, font_path = ["/fonts/ttf"], output=output_pdf)
    except Exception as e:
        st.error(f"Typst compilation failed: {e}")
        st.stop()

    # Read the generated PDF file
    with open(output_pdf, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()

    if pdf_bytes:
                # Display subheader and download button
        st.subheader("Generated Resume")
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=f"Tailored_Resume_{current_date}_{role}.pdf",
            mime="application/pdf")
