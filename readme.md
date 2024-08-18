# Pragmatic Element Plan

## Introduction
Most BIM requirements are currently scattered across poorly structured Excel or Word files, making them difficult to maintain, inconsistent, and challenging to follow or verify. These fragmented requirements often lose alignment with a company's value creation processes, leading to inefficiencies and misaligned business objectives.

This open-source project takes a different approach by offering an interface to define a more structured, accessible, and purpose-driven set of guidelines for geometric modeling and attribution.

## Project Overview
This project consists these main components:

**1. A Viewer for Modeling Guidelines**

A user-friendly viewer that allows stakeholders to easily communicate, access, navigate, and understand the BIM modeling guidelines. This viewer presents the guidelines in a clear and structured manner, ensuring that they are easy to follow and apply consistently across organizations and projects. 

To create your own instance clone the Github project and adapt to your specific needs.

**2. A Structured Approach for Defining Requirements**

BIM requirements often become disconnected from business value, reducing them to mere wish lists. To address this, we’ve designed the project around the principle that every requirement must have a clear purpose, an accountable owner, and actionable workflows.

Our approach begins with:

- Defining the Purpose and Workflow: Start by identifying the purpose and workflow that the requirement supports.
- Assigning Responsibility: Specify who should deliver the information and in which model or file.
- Detailing Requirements: Outline what needs to be modeled and at what quality to achieve the desired outcome.
- Specifying Attributes: Identify the necessary attributes to achieve the business value.

This structured approach is reflected in the database design with core tables for:
- Workflows
- Models
- Elements
- Attributes
To get started, create your own database in the tool of your choice—whether it's Excel, Airtable, or another solution. 




## Installation and Setup

1. **Fork the Repository**  
   Fork the project on GitHub with a unique name, such as `ElementPlan_Your_Organization`.

2. **Run the Code Locally**
   - Open the project folder in your programming environment.
   - Ensure all required libraries are installed.
   - Start the web application by running:  
     ```bash
     streamlit run home.py
     ```

3. **Deploy the Frontend**
   - **Quick Deployment**: Create an account on Streamlit and connect it to your forked repository for easy deployment.
   - **Scalable Deployment**: For more robust needs, consider deploying the service on Azure or any web hosting service that supports Python.
   - **Managed Deployment**: If you prefer a hands-off approach, Abstract Ltd. offers services for hosting and scaling the application.

    

## Usage Instructions

To create a new version of an element plan, follow these steps:

1. **Export Required CSV Files**:  
   Export the following CSV files from your database, ensuring that all necessary columns are included:
   - `Attributes-ExportAll.csv`
   - `Elements-ExportAll.csv`
   - `Models-ExportAll.csv`
   - `Workflows-ExportAll.csv`  
   (Refer to the "Attribute Table" section for details on the required columns.)

2. **Create a New Version Folder**:  
   In the `data\` directory, create a new folder named after the version you're working on (e.g., `data\V2.05`).

3. **Place the CSV Files**:  
   Move the exported CSV files into the newly created version folder.

4. **Run the Merge Script**:  
   Execute the script located at `utils/import_csv.py`. This will generate a merged Excel file containing all the data.

5. **Generate Formatted Files for Contracts**:  
   Run the script at `utils/create_formated_excel_export.py`. This script will create the formatted files required for download and use in contracts.


ToDO: create a admin page to ease this workflow

## Database Configuration

You can use any database tool of your choice (e.g., Excel, Airtable, etc.), but ensure it follows this structure. Note: To add more languages, simply append a new column with the appropriate language code, such as AttributDescriptionSP.

### Attribute Table

- **AttributID (str, int, float)**: A unique identifier for the attribute, e.g., `123` or  the pattern `{AttributName}_{Element_Name}` e-g. '`LongName_space`.
- **AttributName (str)**: The name or type of the attribute, e.g., `Name`, `LongName`, `IsExternal`.
- **SortAttribut (int, float)**: A numerical value used to sort or order the attributes.
- **AttributDescription* (text)**: A description of the attribute the wildcard * stands for the two letter language Shortcut. e.g. AttributDescriptionEN for English
- **Pset (str)**: The property set to which the attribute belongs.
- **AllowedValuesEN (str)**: Comma-separated list of allowed values in English.
- **AllowedValuesDE (str)**: Comma-separated list of allowed values in German.
- **AllowedValuesFR (str)**: Comma-separated list of allowed values in French.
- **AllowedValuesIT (str)**: Comma-separated list of allowed values in Italian.
- **RegexCheckEN (str)**: Regular expression used to validate the attribute in English.
- **RegexCheckDE (str)**: Regular expression used to validate the attribute in German.
- **RegexCheckFR (str)**: Regular expression used to validate the attribute in French.
- **RegexCheckIT (str)**: Regular expression used to validate the attribute in Italian.
- **DataTyp (IfcDatatyp)**: Data type of the attribute’s value, e.g., `IfcLabel`.
- **Unit (str)**: Unit of measurement for the attribute, if applicable, e.g., `sqm`.
- **IFC2x3 (bool)**: Indicates if the attribute is compliant with IFC (Industry Foundation Classes) 2x3 standards.
- **IFC4 (bool)**: Indicates if the attribute is compliant with IFC 4 standards.
- **IFC4.3 (bool)**: Indicates if the attribute is compliant with IFC 4.3 standards.
- **Applicability (bool)**: Indicates if the attribute is used as an IDS Applicability.
- **ElementID (str)**: Identifier for the related element. Use a comma-separated list to link to multiple elements.
- **ModelID (str)**: Identifier for the model to which this attribute applies. Use a comma-separated list to link to multiple models.
- **WorkflowID (str)**: Identifier for the workflow or process associated with this attribute. Use a comma-separated list to link to multiple workflows.


## Contributing
We welcome contributions from the community! If you're a programmer looking to contribute, here are some ways you can get involved:

1. Code Review and Testing
- Code Review: Help us improve the quality of our codebase by reviewing pull requests. Look for bugs, suggest optimizations, and ensure consistency with our coding standards.
- Write Tests: Increase our test coverage by writing unit tests, integration tests, or end-to-end tests. This helps ensure that the code is robust and maintains functionality as the project evolves.
2. Implement New Features
- Feature Suggestions: If you have ideas for new features, feel free to suggest them. You can do this by opening an issue on GitHub with a detailed description of the feature and its potential impact.
- Work on Open Issues: Check out the GitHub Issues to find features or bugs that need attention. Feel free to assign yourself an issue and submit a pull request once you're done.
3. General Suggestions and Feedback
- Use the project and provide feedback. Your experiences and insights can help us make the project better for everyone.

If you are not a Programmer:
1. Improve Documentation and Sample Workflows
- Documentation: Our documentation is crucial for helping new users and contributors get started. Help us expand or refine it by adding new content, fixing errors, or clarifying existing sections.
- Create and share sample workflows that can be included in the documentation or as part of the project examples. This aids users in understanding the practical applications of the project.
2. General Suggestions and Feedback
- Use the project and provide feedback. Your experiences and insights can help us make the project better for everyone.



## FAQ


## Roadmap
1. MVP version 
2. Admin page for non tec

## Community and Support
[How to engage with the community...]

## License
[Details on the project license...]

## Acknowledgements
[Recognition of contributors and tools...]

