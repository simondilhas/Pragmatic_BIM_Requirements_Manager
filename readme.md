# Pragmatic BIM Requirements Manager:
Streamlining BIM Data Management

## Table of Contents
- [Introduction](#introduction)
  - [The Challenge](#the-challenge)
  - [Our Solution](#our-solution)
  - [Use Cases: How This Tool Empowers Client Organizations](#use-cases-how-this-tool-empowers-client-organizations)
- [Project Overview](#project-overview)
- [Usage Instructions](#usage-instructions)
  - [Set up the database in the tool of your choice](#set-up-the-database-in-the-tool-of-your-choice)
  - [Populate the database with a Master Version](#populate-the-database-with-a-master-version)
  - [Create a New Master Version](#create-a-new-master-version)
  - [Manage different versions](#manage-different-versions)
  - [Create Project Versions from the Master Version Template](#create-project-versions-from-the-master-version-template)
- [Installation and Setup](#installation-and-setup)
  1. [Fork the Repository](#1-fork-the-repository)
  2. [Clone and Run Locally](#2-clone-and-run-locally)
  3. [Secure Your Branch](#4-secure-your-branch)
  4. [Deployment Options](#5-deployment-options)
  5. [Stay Updated](#6-stay-updated)
- [Usage Instructions](#usage-instructions)
- [Database Configuration / Required Columns Descriptions](#database-configuration--required-columns-descriptions)
  - [Workflows Columns](#workflows-columns)
  - [Models Columns](#models-columns)
  - [Elements Columns](#elements-columns)
  - [Attributes Columns](#attributes-columns)
  - [Mapping Columns](#mapping-columns)
- [Contributing](#contributing)
- [Architectural Decision Records](#architectural-decision-records)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
### The Challenge

Building Information Modeling (BIM) is crucial in modern design and construction, yet managing BIM requirements ane benefiting form BIM Data remains complex:

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
*Mapping is not necessary for the definition process

## Usage Instructions

### Set up the database in the tool of your choice.
Options include:
   - Airtable (recommended)
   - Excel
   - Other database management systems

### Populate the database with a Master Version
A Master Version is the template to create project specific versions with more or less data.
Recommended Naming Schema: 
   - Master Template Version e.g. `V0.9` 
   - Project Versions e.g. `V0.9-{YOUR PROJECT NUMBER}` e.g. `V0.9-14414`

   1. Define the workflow: Outline the purpose and intended use of your data
   2. Create the container - the file - the IFC Model you expect your data in
   3. Add necessray logical elements(e.g., walls, floors, rooms). Keep in mind that the Ifc Entity is not equal to an element. Think along the lines, of what you have to define in a modeling guidline.
   4. Define necessary attributes: List required attributes for each logical element (at least one per element, otherwiese the code won't process them at the moment)
   5. Connect tables: Link all tables bottom-up, starting from the attribute level
   6. Specify data usage (if needed): Detail how to use the data in the mapping table

### Create a New Master Version

   - **Option 1: quick and dirty in the code:**
      - Export the following CSV files from your database, ensuring that all necessary columns are included (Refer to the "Attribute Table" section for details on the required column.):
         - `M_Attributes.csv`
         - `M_Elements.csv`
         - `M_Models.csv`
         - `M_Workflows.csv`  
      
      - In the `data\` directory, create a new folder named after the version you're working on (e.g., `data\V2.05`).
      - Move the exported CSV files into the newly created version folder.
      - Execute the script located at `src/batch_processing_import.py`. This will generate a merged Excel file containing all the data aswell as different output formats.

   - **Option 2: Upload through the frontend**
      - A more scaleable solution is to use the `admin`page to upload new versions to a blob storage 

### Manage different versions
We recommend the following workflow to manage different versions:
   1. Create the first version.
   2. Deploy the data first on a staging area, to see how it will look.
   3. Once satisfied, deploy on the productive system.
   4. Freeze the version and copy it.
   5. Continue working on the new version.

### Create Project Versions from the Master Version Template
TODO

## Installation and Setup
To create a new version of the project, follow these steps:

### 1. Fork the Repository
Create a fork of the project on GitHub:

**Public:**
- Go to the [original repository](https://github.com/simondilhas/Pragmatic_BIM_Requirements_Manager)
- Clone the original repository and push to your private one

**Privat:**
Detailed instructions for creating a private fork:
- Create a new private repository (e.g., `Private_Pragmatic_BIM_Requirements`)
- Go to your terminal and execute the codes (the capital letters need to be replaced with your data)

```bash
# Clone the original repository as a bare repository
git clone --bare https://github.com/simondilhas/Pragmatic_BIM_Requirements_Manager.git

# Navigate into the cloned repository
cd Pragmatic_BIM_Requirements_Manager.git

# Mirror-push to your new private repository
git push --mirror https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

# Remove the temporary local repository
cd ..
mac:
rm -rf Pragmatic_BIM_Requirements_Manager.git
windows:
Remove-Item -Recurse -Force Pragmatic_BIM_Requirements_Manager.git

# Clone your new private repository
git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

# Navigate into your new repository
cd YOUR_REPOSITORY_NAME

# Add the original repository as a remote to fetch updates
git remote add upstream https://github.com/simondilhas/Pragmatic_BIM_Requirements_Manager.git
```

### 2. Clone and Run Locally
```bash
pip install -r requirements.txt
streamlit run home.py
```

### 4. Secure Your Branch

To implement basic password protection:

1. Run `src/create_hashed_pw.py`:
   - Set your desired password in this script.
   - **IMPORTANT:** Remove the password from the script before committing to GitHub.

2. Create the file `.streamlit/secrets.toml`.

3. Add the generated hash to `secrets.toml`:
   ```toml
   hashed_password = "YOUR_GENERATED_HASH_HERE"
   ```

4. Ensure `.streamlit/secrets.toml` is listed in your `.gitignore` file.

**Security Notice:**

This method provides basic protection but is not suitable for high-security applications.
For production environments, consider implementing:

- Robust user management system e.g. Azure Active Directory (Azure AD)
- Two-factor authentication (2FA)
- Secure session handling

### 5. Deployment Options
 - Quick: Use Streamlit Share (https://streamlit.io/sharing) for easy cloud deployment
 - Scalable: Deploy on cloud platforms like Azure, AWS, or GCP. On Azure we recommend:
   - Webapp or Docker app
   - Blob storage for the versions.
   - Active Directory to manage logins
 - Managed: Contact Abstract Ltd. for hosted solutions

### 6. Stay Updated
 Regularly sync with the original repository:
```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

or to do it simpler
- Go to your new project
- execute once:
```bash
git config --global alias.sync '!git checkout main && git fetch upstream && git merge upstream/main && git push origin main'
```
- when you just have to run to fetch the updates and merge with your instance
```bash
git sync
```

### 7. Configure the projects

- use the `.env` file to setup your keys, the `.env.template` file gives the structure
- use the `config.yaml`for general setup options


## Database Configuration / Required Columns Descriptions

You can use any database tool of your choice (e.g., Excel, Airtable, etc.), but ensure it follows this structure. Note: To add more languages, simply append a new column with the appropriate language code, such as AttributeDescription.

#### Workflows Columns

- **WorkflowID (str, int)**: A unique identifier for the workflow.
- **WorkflowName\* (str)**: The name of the workflow in the specified language, e.g., `WorkflowNameEN` for English.
- **WorkflowSubheader\* (str)**: A subheader for the workflow, providing additional context or categorization, e.g., `WorkflowSubheaderEN` for English.
- **WorkflowDescription\* (text)**: A detailed description of the workflow in the specified language, e.g., `WorkflowDescriptionEN` for English.
- **Status (str)**: Indicates the current status of the workflow, such as `Active`, `Inactive`, or `Pending`.

#### Models Columns

- **ModelID (str, int)**: A unique identifier for the model. e.g. ARC-Model
- **ModelName\* (str)**: The name of the model in the specified language, e.g., `ModelNameEN` for English.
- **ModelDescription\* (text)**: A detailed description of the model in the specified language, e.g., `ModelDescriptionEN` for English.
- **FileName\* (str)**: The name of the file associated with the model in the specified language, e.g., `FileNameEN` for English.
- **SortModels (int, float)**: A numerical value used to sort or order the models.

#### Elements Columns

- **ElementID (str)**: A unique identifier for the element e.g., `123` or a pattern like `{ElementName}_{ModelName}`, e.g., `Space_ARC-Model`.
- **ElementName\* (str)**: The name of the element in the specified language, e.g., `ElementNameEN` for English.
- **SortElement (int, float)**: A numerical value used to sort or order the elements.
- **IfcEntityIfc4.0Name (str)**: The name of the IFC (Industry Foundation Classes) entity associated with the element, compliant with IFC 4.0 standards.
- **ElementDescription\* (text)**: A detailed description of the element in the specified language, e.g., `ElementDescriptionEN` for English.

#### Attributes Columns

- **AttributeID (str, int)**: A unique identifier for the attribute, e.g., `123` or a pattern like `{AttributeName}_{ElementName}`, e.g., `LongName_space`.
- **AttributeName (str)**: The name or type of the attribute, e.g., `Name`, `LongName`, `IsExternal`.
- **SortAttribute (int, float)**: A numerical value used to sort or order the attributes.
- **AttributeDescription* (text)**: A description of the attribute in the specified language, e.g., `AttributeDescription` for English.
- **Pset (str)**: The property set to which the attribute belongs.
- **AllowedValues\* (str)**: Comma-separated list of allowed values in the specified language, e.g., `AllowedValuesEN` for English.
- **RegexCheck\* (str)**: Regular expression used to validate the attribute in the specified language, e.g., `RegexCheckEN` for English.
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
We welcome contributions from everyone—whether you’re a seasoned developer, new to open-source or have domain knowledge. Your input is invaluable in making this project better for everyone.

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

## Architectural Decision Records
The main architectural decisions are documented in `adr\`. Please consider these and consult when making major changes.

## FAQ
ToDo: Add FAQ

## Roadmap
1. MVP version ... work in Progress
2. Admin page for non tec ... work in Progress
3. IDS creation ... work in Progress


## License
This project is licensed under the GNU Lesser General Public License (LGPL).

What This Means for Users:

- Freedom to Use: You are free to use this software for personal, academic, or commercial purposes without any restrictions.
- Modification and Distribution: You can modify the source code and distribute your modified versions, provided that you also distribute the modifications under the same LGPL license.
- Integration with Proprietary Software: Unlike the full GNU General Public License (GPL), the LGPL allows you to link this library with proprietary software without requiring that the proprietary software itself be open-sourced.
- Contribution Back: If you improve or modify the library, we encourage (but do not require) you to contribute your changes back to the community, so everyone can benefit from your enhancements.

For full details, please see the LICENSE.txt file included in the repository (https://github.com/simondilhas/Pragmatic_BIM_Requirements_Manager).

## Acknowledgements
I would like to extend my heartfelt appreciation to everyone who contributed to the success of this project:

- Open Source Libraries: My sincere thanks go to the developers and contributors of Streamlit, Pandas, and Plotly. Your open-source tools have been essential in the development of this project.

- Pierre Monico: I am deeply grateful for your continued support and coding advice. Your insights and guidance have been invaluable throughout this process.

- Requirment Definition Projects: Over the past years, I have had the privilege of simplifying the requirement definition process for various projects. The experience gained from these efforts has been instrumental to set up this project.
