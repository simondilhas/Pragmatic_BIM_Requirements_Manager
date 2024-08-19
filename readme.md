# Pragmatic Element Plan

## Introduction
# BIM Requirements Manager: Streamlining BIM Data Management

### The Challenge

Building Information Modeling (BIM) is crucial in modern construction, yet managing BIM requirements remains complex:

1. Client BIM requirements are dispersed across multiple, disconnected documents.
2. Requirement inconsistencies impede the development of automated BIM data workflows.
3. Companies resort to custom solutions (often Excel-based), but lack resources for optimal implementation.

Current solutions like BuildingSMART's data dictionary and Information Delivery Specification (IDS) primarily address metadata requirements. Plannerly, while comprehensive, focuses more on project execution than data handover and requirement formulation.

### Our Solution

Introducing our lightweight, open-source web application designed for efficient and pragmatic BIM requirements management:

#### Key Features

1. **Freedom and Flexibility through Open Source Licensing**: Adapt, modify, and extend the tool to meet your specific workflow needs.
2. **Customization and Extension**: Tailor the tool to your project's / organizations unique needs.
3. **Multi-view Communication**: Deliver requirements in stakeholder-specific formats:
   - Searchable web interface for Modelers
   - Excel contract documents for Project Managers
   - IDS or BIMCollab ZOOM Smart Views for BIM Managers
4. **Backend Flexibility**: Work with familiar databases (Excel, Airtable, MS Access, etc.) for requirement production.
5. **Flexible Licensing**:
   - Self-hosting for complete control
   - Full-service option for managed solutions

Simplify your BIM data management and maximize your project's potential with our versatile, user-friendly solution!

### Use Cases: How This Tool Empowers Client Organizations

This tool is primarily designed to support government and large client organizations in defining and communicating their BIM data requirements effectively. With over five years of experience working with diverse database solutions, we have crafted a tool that addresses the specific needs of our clients. Here’s how it is being utilized:

1. **Custom Requirement Definition:** Clients can tailor BIM requirements to align with their unique data needs, ensuring that the information collected is relevant and actionable for their specific projects.

2. **Streamlined Data Documentation:** The tool facilitates the documentation of data post-processing steps, ensuring a smooth and efficient handover process within their systems, reducing the risk of data loss or misinterpretation.

3. **Effective Communication of Data Needs:** By using this tool, clients can clearly communicate their data requirements to planners and contractors, ensuring that everyone involved in the project is on the same page and working towards the same data goals.

This structured approach not only improves efficiency but also enhances the alignment of BIM data with the strategic objectives of the organization, leading to better project outcomes.

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

       +-----------------+
       |    Workflows    |<---
       +-----------------+   |
                             |
       +-----------------+   |
       |      Models     |<--|
       +-----------------+   |
                             |
       +-----------------+   |
       |     Elements    |<--|
       +-----------------+   |
                             |  
       +-----------------+   |   +-----------------+
       |   Attributes    |---|-->|     Mapping*    |
       +-----------------+       +-----------------+


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

## Database Configuration / Required Columns Descriptions

You can use any database tool of your choice (e.g., Excel, Airtable, etc.), but ensure it follows this structure. Note: To add more languages, simply append a new column with the appropriate language code, such as AttributDescriptionEN.

#### Workflows Columns

- **WorkflowID (str, int)**: A unique identifier for the workflow.
- **WorkflowName* (str)**: The name of the workflow in the specified language, e.g., `WorkflowNameEN` for English.
- **WorkflowSubheader* (str)**: A subheader for the workflow, providing additional context or categorization, e.g., `WorkflowSubheaderEN` for English.
- **WorkflowDescription* (text)**: A detailed description of the workflow in the specified language, e.g., `WorkflowDescriptionEN` for English.
- **Status (str)**: Indicates the current status of the workflow, such as `Active`, `Inactive`, or `Pending`.

#### Models Columns

- **ModelID (str, int)**: A unique identifier for the model. e.g. ARC-Model
- **ModelName* (str)**: The name of the model in the specified language, e.g., `ModelNameEN` for English.
- **ModelDescription* (text)**: A detailed description of the model in the specified language, e.g., `ModelDescriptionEN` for English.
- **FileName* (str)**: The name of the file associated with the model in the specified language, e.g., `FileNameEN` for English.
- **SortModels (int, float)**: A numerical value used to sort or order the models.

#### Elements Columns

- **ElementID (str)**: A unique identifier for the element e.g., `123` or a pattern like `{ElementName}_{ModelName}`, e.g., `Space_ARC-Model`.
- **ElementName* (str)**: The name of the element in the specified language, e.g., `ElementNameEN` for English.
- **SortElement (int, float)**: A numerical value used to sort or order the elements.
- **IfcEntityIfc4.0Name (str)**: The name of the IFC (Industry Foundation Classes) entity associated with the element, compliant with IFC 4.0 standards.
- **ElementDescription* (text)**: A detailed description of the element in the specified language, e.g., `ElementDescriptionEN` for English.

#### Attributes Columns

- **AttributID (str, int)**: A unique identifier for the attribute, e.g., `123` or a pattern like `{AttributName}_{ElementName}`, e.g., `LongName_space`.
- **AttributName (str)**: The name or type of the attribute, e.g., `Name`, `LongName`, `IsExternal`.
- **SortAttribut (int, float)**: A numerical value used to sort or order the attributes.
- **AttributDescription* (text)**: A description of the attribute in the specified language, e.g., `AttributDescriptionEN` for English.
- **Pset (str)**: The property set to which the attribute belongs.
- **AllowedValues* (str)**: Comma-separated list of allowed values in the specified language, e.g., `AllowedValuesEN` for English.
- **RegexCheck* (str)**: Regular expression used to validate the attribute in the specified language, e.g., `RegexCheckEN` for English.
- **DataTyp (IfcDatatyp)**: The data type of the attribute’s value, e.g., `IfcLabel`.
- **Unit (str)**: Unit of measurement for the attribute, if applicable, e.g., `sqm`.
- **IFC2x3 (bool)**: Indicates if the attribute is compliant with IFC 2x3 standards.
- **IFC4 (bool)**: Indicates if the attribute is compliant with IFC 4 standards.
- **IFC4.3 (bool)**: Indicates if the attribute is compliant with IFC 4.3 standards.
- **Applicability (bool)**: Indicates if the attribute is used as an IDS Applicability.
- **ElementID (str)**: Identifier for the related element. Use a comma-separated list to link to multiple elements.
- **ModelID (str)**: Identifier for the model to which this attribute applies. Use a comma-separated list to link to multiple models.
- **WorkflowID (str)**: Identifier for the workflow or process associated with this attribute. Use a comma-separated list to link to multiple workflows.

#### Mapping Columns

- **MappingID (str)**: A unique identifier for the mapping rule or process associated with this mapping.
- **Description (text)**: A detailed description of the mapping and it's purpose. This text explains the purpose, scope, or other relevant information about the workflow. For example, `Mapping of SIA416 classified areas to SAP `
- **TargetSystem**: Names the target System e.g. `SAP S/4HANA`
- **IfcAttributIDs (str)**: A comma-separated list of unique identifiers for the attributes involved in this workflow. Each ID corresponds to an attribute that is part of the mapping logic. For example, `Area_Space, SIA_416_Classification`.
- **CalculationLogic (text)**: A textual description or formula that outlines the logic used to calculate or process the attributes within the workflow. This helps the programmer to set up the actual workflow. e.g. Sum of all Area_Space if they are HNF

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
ToDo: Add FAQ

## Roadmap
1. MVP version ... work in Progress
2. Admin page for non tec
3. IDS creation


## License
This project is licenced under GNU LESSER GENERAL PUBLIC LICENSE, for Details see LICENCE.txt

## Acknowledgements
I would like to extend my heartfelt appreciation to everyone who contributed to the success of this project:

- Open Source Libraries: My sincere thanks go to the developers and contributors of Streamlit, Pandas, and Plotly. Your open-source tools have been essential in the development of this project.

- Pierre Monico: I am deeply grateful for your continued support and coding advice. Your insights and guidance have been invaluable throughout this process.

- Requirment Definition Projects: Over the past years, I have had the privilege of simplifying the requirement definition process for various projects. The experience gained from these efforts has been instrumental to set up this project.
