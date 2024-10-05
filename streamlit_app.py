import streamlit as st
import anthropic
import json
from datetime import datetime
import os
import typst
import PyPDF2

# --- Your Original Resume (replace with your actual content) ---
original_resume = """
= Peerapat Chiaprasert (Chin)
peerapat.chiaprasert\@gmail.com |
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
*TiffinLabs*#h(1fr) Mar 2022 -- Oct 2023 \
*Country General Manager*
- Expanded TiffinLabs' delivery-centric brand to 100 storefronts in Thailand. Led and developed the entire business team, overseeing marketing, business development, and operations. Streamlined processes for efficient growth and market penetration.
- Developed product value propositions for 7 delivery-focused food brands. Defined brand roadmaps ensuring product-market fit and established processes to capture evolving trends. Continuously refined offerings based on consumer feedback.
- Boosted GMV by 20% monthly through strategic marketing collaborations with delivery platforms. Maximized NPD sales by aligning promotional efforts and implementing regular product enhancements through agile methodology.
- Achieved 15% COGS reduction by initiating fulfillment partnerships with distributors. Negotiated favorable terms to meet target pricing and quality standards. Improved sourcing processes, resulting in faster procurement and increased efficiency.

*Grab*#h(1fr) Jun 2017 -- Feb 2022 \
*Head, GrabKitchen* (2019-2022)
- Established Thailand's largest cloud kitchen network, GrabKitchen, developing an asset-lite model. Secured partnership with top F&B company CRG, creating a scalable, profitable business model for long-term growth.
- Grew GMV by average 25% per month and achieved 4x ROI through strategic marketing campaigns. Managed thematic promotions, partnerships, and Joint Business Plans to drive customer engagement and increase platform usage.
- Created a data-driven model for selecting profitable expansion locations. Utilized past performance data and location-specific demand trends to calculate individual kitchen profitability and determine accurate payback periods.
- Managed a diverse portfolio exceeding 400 million THB in annual GMV. Oversaw 120+ F&B accounts, including street vendors, local chains, QSRs, and strategic partners, ensuring optimal selections across segments to maximize growth
*Operations Manager, GrabFood | Special Project Lead, GrabBike & GrabExpress* (2017-2019)
- Propelled GrabFood to market leadership within 8 months through strategic initiatives. Established and optimized key functions including fleet management, business development, revenue collection, and customer services.
- Developed e-commerce strategies for leading F&B brands. Designed tailored solutions to launch and grow online channel for major brands such as MK, Starbucks, and CRG, driving online growth and enhancing market competitiveness
- Built and mentored high-performing teams across various functions and locations.  Oversaw 100+ staff members, including 7 direct reports, fostering a culture of excellence and continuous improvement throughout the organization.

*Ipsos Business Consulting*#h(1fr) Jul 2016 -- May 2017 \
*Associate Consultant*
- Developed e-payment business model and identified strategic partners for successful launch. Utilized insightful market data to shortlist potential collaborators, ensuring a strong foundation for the new venture.
- Designed go-to-market strategy for Thai financial institution's e-commerce launch. Conducted comprehensive market research and analysis to inform strategic decisions and optimize market entry approach.
*EY (Ernst & Young)* #h(1fr) Feb 2015 -- Jun 2016 \
*Consultant*
- Created costing model to pinpoint service costs and address profitability issues for Ministry of Public Health hospitals nationwide. Analyzed data to identify root causes and areas for financial improvement and efficiency gains.
- Enhanced efficiency for listed manufacturing company through business process improvement. Recommended new flow charts, SOPs, and integrated ERP systems to streamline operations and boost overall productivity.
== EDUCATION
#chiline()
*Thammasat University* #h(1fr) Jun 2011 -- Dec 2014 \
Bachelor of Accounting (International Program)
"""

# --- Anthropic API Setup ---
client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY") 

# --- Typst Font Path Setup ---
typst_font_path = "/fonts/ttf"  

# --- Function to tailor the resume ---
def tailor_resume(resume_text, job_description, role):
    try:
        message=client.messages.create( 
                model="claude-3-5-sonnet-20240620",
                max_tokens=8192,
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""You are an AI assistant tasked with analyzing a resume and a job description to create customized content for a job application. Your goal is to provide truthful and relevant information based solely on the given resume while tailoring it to the specific job requirements. It is crucial that you do not invent or add any information that is not present in or cannot be directly inferred from the original resume. Stick closely to the content and tone of the original document.

            First, carefully read and analyze the following documents:

            <resume>
            {original_resume}
            </resume>

            <job_description>
            {job_description}
            </job_description>

            After analyzing both documents, you will create customized content in three parts:

            1. Profile Summary:
            Create a 2-3 sentence statement that explains the candidate's years of experience, industry expertise, and highlights the most relevant skills for the job. Ensure that all information is truthful and can be directly referenced from the original resume. Tailor this summary to match the requirements in the job description.

            2. Key Achievements:
            List 3 bullet points, each showing an achievement from past experience that provides solid evidence for the profile summary. These achievements should be directly taken from the resume and should be relevant to the job description. Use exact phrases from the resume whenever possible.

            3. Areas of Expertise:
            Provide a list of 12 skills that are most relevant to the job description. These skills should be explicitly mentioned in the resume and align closely with the requirements listed in the job description. Prioritize using exact terms from the original resume.

            After generating each section, compare it to the original resume and ensure that at least 90% of the content can be directly traced back to the original document. Only make minimal inferences when absolutely necessary. If you must infer information, it should be a logical and direct conclusion from explicitly stated facts in the resume.

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

            After completing the analysis, review each point in your output and provide a brief justification for its inclusion by referencing the specific part of the original resume it came from. This justification should be included as an additional field in the JSON output.

            Remember to provide only truthful information that can be referenced from or minimally inferred from the original resume. Ensure that all content is tailored to match the requirements specified in the job description while maintaining a high degree of fidelity to the original resume."""
                            }
                        ]
                    }
                ]
            )

            # Print the response
        print(message.content)

        tailored_content = message.content[0].text if message.content else None
        data = json.loads(tailored_content) if tailored_content else None

        if data:
            profile_summary = data.get('profile_summary', '')
            key_achievements = data.get('key_achievements', [])[:3]
            areas_of_expertise = data.get('areas_of_expertise', [])[:12]

            # --- Typst Template Population ---
            template = f"""
            #set text(font: "inter",size: 8.5pt, hyphenate: true, ligatures: false, weight: "regular")
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
            peerapat.chiaprasert\@gmail.com |
            #link("https://linkedin.com/in/chpeerapat")[linkedin.com/in/chpeerapat] |
            (+66)86-624-6630 | Bangkok, Thailand]
            == PROFILE SUMMARY
            #chiline()
            *{profile_summary}*
            - {key_achievements[0] if key_achievements else ''}
            - {key_achievements[1] if len(key_achievements) > 1 else ''}
            - {key_achievements[2] if len(key_achievements) > 2 else ''}
            == AREAS OF EXPERTISE
            #chiline()
            #columns(3)[
            #align(center)[
                {areas_of_expertise[0] if areas_of_expertise else ''}\\
                {areas_of_expertise[1] if len(areas_of_expertise) > 1 else ''}\\
                {areas_of_expertise[2] if len(areas_of_expertise) > 2 else ''}\\
                {areas_of_expertise[3] if len(areas_of_expertise) > 3 else ''}
            ]
            #colbreak()
            #align(center)[
                {areas_of_expertise[4] if len(areas_of_expertise) > 4 else ''}\\
                {areas_of_expertise[5] if len(areas_of_expertise) > 5 else ''}\\
                {areas_of_expertise[6] if len(areas_of_expertise) > 6 else ''}\\
                {areas_of_expertise[7] if len(areas_of_expertise) > 7 else ''}
            ]
            #colbreak()
            #align(center)[
                {areas_of_expertise[8] if len(areas_of_expertise) > 8 else ''}\\
                {areas_of_expertise[9] if len(areas_of_expertise) > 9 else ''}\\
                {areas_of_expertise[10] if len(areas_of_expertise) > 10 else ''}\\
                {areas_of_expertise[11] if len(areas_of_expertise) > 11 else ''}
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
            """.strip()

            # Compile Typst to PDF
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename_base = f"Peerapat Chiaprasert Resume-{current_date}-{role}"
            typst_filename = filename_base + ".typ"
            pdf_filename = filename_base + ".pdf"

            with open(typst_filename, "w", encoding="utf-8") as file:
                file.write(template) 

            typst.compile(typst_filename, font_paths=[typst_font_path], output=pdf_filename)

            return template, pdf_filename  

        else:
            raise ValueError("AI analysis failed to produce valid output.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# --- Streamlit App ---
st.title("AI-Powered Resume Tailor")

resume_text = st.text_area("Paste Your Resume Here:", value=original_resume)
role = st.text_input("Enter the Target Job Role:", value="e.g., Data Scientist")
job_description = st.text_area("Paste the Job Description:")

if st.button("Tailor My Resume"):
    if resume_text and job_description and role:
        with st.spinner("Analyzing and Tailoring..."):
            tailored_resume_content, pdf_filename = tailor_resume(
                resume_text, job_description, role
            )

            if tailored_resume_content and pdf_filename:
                st.success("Resume Tailored Successfully!")

                st.subheader("Tailored Resume Preview:")
                st.write(tailored_resume_content) 

                with open(pdf_filename, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(label="Download Tailored Resume", 
                                   data=pdf_bytes,
                                   file_name=pdf_filename)

                os.remove(pdf_filename)
    else:
        st.warning("Please provide your resume, job role, and the job description.") 