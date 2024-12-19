import pandas as pd

# Define the dictionary to map directories to sample content for missing columns
directory_to_content = {
    "ACCOUNTANT": {
        "Work Experience": "2+ years as an accountant in a corporate firm",
        "Education": "Bachelor's degree in Accounting",
        "Skills": "Excel, QuickBooks, Financial Analysis",
        "Languages": "English, French"
    },
    "ADVOCATE": {
        "Work Experience": "5+ years as a corporate advocate specializing in civil law",
        "Education": "Law Degree from XYZ University",
        "Skills": "Legal Research, Litigation, Negotiation",
        "Languages": "English, Arabic"
    },
    "AGRICULTURE": {
        "Work Experience": "3+ years in agricultural management and farming",
        "Education": "Bachelor's degree in Agriculture",
        "Skills": "Farm Management, Crop Rotation, Pest Control",
        "Languages": "English, French"
    },
    "APPAREL": {
        "Work Experience": "4+ years working in fashion design and apparel manufacturing",
        "Education": "Bachelor's degree in Fashion Design",
        "Skills": "Design, Pattern Making, Textile Knowledge",
        "Languages": "English, Italian"
    },
    "ARTS": {
        "Work Experience": "5+ years as a visual artist specializing in abstract art",
        "Education": "Master's in Fine Arts from ABC University",
        "Skills": "Painting, Sculpture, Digital Art",
        "Languages": "English, French"
    },
    "AUTOMOBILE": {
        "Work Experience": "3+ years in automobile sales and customer service",
        "Education": "Bachelor's degree in Automotive Engineering",
        "Skills": "Vehicle Diagnostics, Sales, Customer Relations",
        "Languages": "English, Spanish"
    },
    "AVIATION": {
        "Work Experience": "2+ years as a commercial pilot with XYZ Airlines",
        "Education": "Bachelor's in Aviation and Piloting from ABC Academy",
        "Skills": "Flight Operations, Safety Protocols, Aircraft Maintenance",
        "Languages": "English, Arabic"
    },
    "BANKING": {
        "Work Experience": "4+ years in retail banking and financial services",
        "Education": "Bachelor's degree in Finance",
        "Skills": "Customer Service, Loan Management, Risk Assessment",
        "Languages": "English, French"
    },
    "BPO": {
        "Work Experience": "3+ years in BPO operations as a customer support specialist",
        "Education": "Bachelor's degree in Business Administration",
        "Skills": "Customer Support, Telemarketing, Conflict Resolution",
        "Languages": "English, Hindi"
    },
    "BUSINESS-DEVELOPMENT": {
        "Work Experience": "5+ years as a Business Development Manager",
        "Education": "MBA in Business Development",
        "Skills": "Market Research, Sales Strategy, Partnership Management",
        "Languages": "English, Spanish"
    },
    "CHEF": {
        "Work Experience": "8+ years as an executive chef in a fine dining restaurant",
        "Education": "Culinary Arts Degree from ABC Culinary School",
        "Skills": "Menu Creation, Food Preparation, Staff Management",
        "Languages": "English, French"
    },
    "CONSTRUCTION": {
        "Work Experience": "10+ years as a project manager in the construction industry",
        "Education": "Bachelor's degree in Civil Engineering",
        "Skills": "Project Management, Site Supervision, Budgeting",
        "Languages": "English, Spanish"
    },
    "CONSULTANT": {
        "Work Experience": "5+ years as a business consultant specializing in strategy",
        "Education": "MBA in Business Strategy",
        "Skills": "Strategy Formulation, Market Analysis, Client Management",
        "Languages": "English, French"
    },
    "DESIGNER": {
        "Work Experience": "3+ years as a graphic designer for digital media",
        "Education": "Bachelor's degree in Graphic Design",
        "Skills": "Adobe Creative Suite, Typography, User Interface Design",
        "Languages": "English, German"
    },
    "DIGITAL-MEDIA": {
        "Work Experience": "4+ years as a social media manager and content strategist",
        "Education": "Bachelor's degree in Digital Marketing",
        "Skills": "Content Creation, Social Media Marketing, SEO",
        "Languages": "English, Spanish"
    },
    "ENGINEERING": {
        "Work Experience": "6+ years as a software engineer in a tech firm",
        "Education": "Bachelor's degree in Computer Science",
        "Skills": "Programming (Java, Python), Database Management, Agile",
        "Languages": "English, German"
    },
    "FINANCE": {
        "Work Experience": "4+ years as a financial analyst",
        "Education": "Bachelor's degree in Finance",
        "Skills": "Financial Reporting, Budgeting, Risk Management",
        "Languages": "English, French"
    },
    "FITNESS": {
        "Work Experience": "5+ years as a personal trainer and fitness coach",
        "Education": "Certified Personal Trainer",
        "Skills": "Strength Training, Weight Loss, Nutrition Planning",
        "Languages": "English, Spanish"
    },
    "HEALTHCARE": {
        "Work Experience": "6+ years as a nurse in a hospital setting",
        "Education": "Bachelor's in Nursing",
        "Skills": "Patient Care, Medical Documentation, Emergency Response",
        "Languages": "English, Arabic"
    },
    "HR": {
        "Work Experience": "3+ years in human resources management",
        "Education": "Bachelor's degree in Human Resource Management",
        "Skills": "Recruitment, Employee Relations, Payroll",
        "Languages": "English, Spanish"
    },
    "INFORMATION-TECHNOLOGY": {
        "Work Experience": "5+ years as an IT manager in a multinational company",
        "Education": "Bachelor's degree in Information Technology",
        "Skills": "Network Security, Cloud Computing, IT Support",
        "Languages": "English, German"
    },
    "PUBLIC-RELATIONS": {
        "Work Experience": "4+ years as a public relations manager for a major corporation",
        "Education": "Bachelor's in Public Relations",
        "Skills": "Media Relations, Crisis Communication, Brand Management",
        "Languages": "English, French"
    },
    "SALES": {
        "Work Experience": "3+ years in retail sales management",
        "Education": "Bachelor's degree in Marketing",
        "Skills": "Sales Strategy, Customer Service, Negotiation",
        "Languages": "English, Spanish"
    },
    "TEACHER": {
        "Work Experience": "5+ years as a high school mathematics teacher",
        "Education": "Bachelor's in Education",
        "Skills": "Lesson Planning, Classroom Management, Subject Knowledge",
        "Languages": "English, French"
    }
}

# List of valid languages
valid_languages = {"English", "French", "Spanish", "German", "Italian", "Arabic", "Hindi"}

# Read the CSV dataset
file_path = './cv_data.csv'  
df = pd.read_csv(file_path)

# Function to fill missing values and ensure valid languages
def fill_missing_values(row):
    directory = row['directory']
    if directory in directory_to_content:
        content = directory_to_content[directory]
        row['Work Experience'] = row['Work Experience'] if not pd.isna(row['Work Experience']) else content['Work Experience']
        row['Education'] = row['Education'] if not pd.isna(row['Education']) else content['Education']
        row['Skills'] = row['Skills'] if not pd.isna(row['Skills']) else content['Skills']
        
        # Check if Languages column has a valid value
        if pd.notna(row['Languages']):
            languages = row['Languages'].split(', ') if isinstance(row['Languages'], str) else content['Languages']
        else:
            languages = content['Languages']  # Use the default valid value from the directory_to_content dictionary
        
        # Filter the languages to ensure only valid ones are kept
        languages = [lang for lang in languages if lang in valid_languages]
        row['Languages'] = ', '.join(languages)  # Make sure the languages are joined as a string
    return row

# Apply the function to each row
df = df.apply(fill_missing_values, axis=1)

df = df.drop('filename', axis=1)

# Rename the column
df.rename(columns={'directory': 'Category'}, inplace=True)

# Save the updated dataset back to a CSV file
output_file_path = 'updated_dataset.csv'  # Replace with your desired output file path
df.to_csv(output_file_path, index=False)

print(f"Missing values filled and saved to {output_file_path}")
