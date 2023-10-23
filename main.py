import openai
import streamlit as st
import os
import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle , PageBreak
from reportlab.lib.styles import getSampleStyleSheet

start_time = time.time()

st.title("💼 Business Report Generator")

# Create a form to collect user inputs
with st.form(key='business_info_form'):
    business_idea = st.text_area("Business Idea:", value="my idea is make notes sharing platforms where students study day before sem exam", help="Describe your business idea.")
    business_name = st.text_input("Business Name:", value="College Hive", help="Enter the name of your business.")
    pricing_strategies = st.text_area("Pricing Strategies:", value="basic notes is free", help="Describe your pricing strategies.")

    submit_button = st.form_submit_button(label='Generate Report')

# When the form is submitted
if submit_button:
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Format the business data as a string
    business_data_string = (
        f"Business Idea: {business_idea}\n"
        f"Business Name: {business_name}\n"
        f"Pricing Strategies: {pricing_strategies}\n"
        f"User Attraction Strategy: Example Strategy"  # Placeholder, replace with actual data
    )

    # Define the custom instruction
    custom_instruction = (
        "Prepare a formal business report based on the provided business idea, "
        "name, pricing strategies, and user attraction strategy. Each section of "
        "the report should be 500 words and written in a professional tone."

        ''' this how i would like you to know about topic to provide better responses?


        
        this is business report format
I. Executive Summary:

Company Overview
Industry Background
Problem ,
Solution
II. Industry Analysis:

Market Trends and Dynamics
Competitive Analysis
Regulatory and Compliance Landscape
Socio-Economic Factors
SWOT Analysis
III. Problem and Opportunity Assessment:

Problem Statement
Market Gap Analysis
User Pain Points
Opportunity Analysis
IV. Solution Design and Validation:

Solution Framework
Unique Value Proposition
Market Validation
Proof of Concept Results
V. Technology and Innovation:
Technology Architecture
Tech Stack
AI/ML Implementation
Cybersecurity Measures
Innovation and Intellectual Property
VI. Market Strategy:

Market Research
Customer Segmentation
Consumer Behavior Analysis
Marketing and Sales Strategy
Pricing and Positioning
Channel Strategy
Digital Presence and Strategy
VII. Product Development:

Product Roadmap
MVP Strategy (10 steps of MVP also)
Feature Prioritization
Development Timeline
User Feedback and Iteration
VIII. Operational Plan:

Operational Framework
Risk Assessment and Mitigation
KPIs and Performance Metrics
Organizational Structure
Team and Talent Management
Supply Chain and Logistics
IX. Financial Planning and Analysis:

Revenue Model and Monetization Strategies
Financial Statements
Cash Flow Analysis
Sensitivity Analysis



XII. Social Impact:
Social Responsibility Initiatives
Community Engagement
XIII. Evaluation and Continuous Improvement:

Performance Analysis
Continuous Improvement Strategies
Learning and Adaptation'''

    )

    # Create the messages array for the OpenAI API call
    messages = [
        {"role": "system", "content": custom_instruction},
        {"role": "user", "content": business_data_string}
    ]

    # Make the OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    respone_time = time.time()

    st.write("Time taken to generate response: " + str(respone_time - start_time) + " seconds")

    # with open('generated_report.txt', 'w') as f:
    #     f.write(response)


    generated_report = response['choices'][0]['message']['content']
    # with open('generated_report.txt', 'r') as f:
    #     generated_report = f.read()

    st.write(generated_report)
    filename = 'generated_report'+str(time.time())

    sections = generated_report.split("\n\n")

    output_file = "generated_report.pdf"
    #  Create a PDF document
    doc = SimpleDocTemplate("business_report.pdf", pagesize=letter)

    # Get the sample style sheet
    styles = getSampleStyleSheet()

    # Split your report into sections
    sections = generated_report.split("\n\n")

    # Create an empty list to collect the elements to be added to the PDF
    elements = []

    for section in sections:
        # Add a paragraph with the section content
        elements.append(Paragraph(section, styles['Normal']))
        # Add a page break
        # elements.append(PageBreak())

    # Build the PDF document with the collected elements
    doc.build(elements)

    # save the pdf with file name

    st.write("Report generated successfully! Download the report [here](business_report.pdf).")


    st.write("Report generated successfully! Download the report [here](generated_report.txt).")

    end_time = time.time()

    st.write("Time taken to generate report: " + str(end_time - start_time) + " seconds")


    # with open(filename, 'w') as f:
    #     f.write("Business Report\n")
    #     f.write("Business Idea: " + business_idea + "\n")
    #     f.write("Business Name: " + business_name + "\n")
    #     f.write("Pricing Strategies: " + pricing_strategies + "\n")


    #     f.write(generated_report)