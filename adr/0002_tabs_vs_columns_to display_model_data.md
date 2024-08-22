# Architectural Decision Record (ADR)

**ADR Title:** Choosing Between `st.tabs` and `st.expander` for Displaying Model Data in Streamlit

**Date:** August 22, 2024

---

## Context

We are developing a data-driven application in Streamlit that displays various model outputs and performance metrics. The application needs to present this data in a clear, organized manner, enabling users to navigate through different sections efficiently. 

The two primary options considered for organizing the model data are:

1. **`st.tabs`**: Allows the content to be organized into separate tabs.
2. **`st.expander`**: Provides expandable/collapsible sections for the content.

Key considerations include user experience, display speed, and ease of data comparison across different model outputs.

---

## Options Considered

1. **`st.tabs`**
2. **`st.expander`**

---

## Option 1: `st.tabs`

**Description:**
`st.tabs` in Streamlit allows for organizing content into separate tabs, where each tab can contain different data or visualizations. This option enables users to quickly switch between different datasets or model outputs without the need to scroll or expand sections.

**Pros:**

- **Faster Display**: Content in all tabs is loaded simultaneously, allowing for instant switching between tabs.
- **User Experience**: Provides a more intuitive way to organize and access different sections of model data, especially when comparing different outputs.
- **Cleaner Interface**: Tabs reduce the need for scrolling, creating a cleaner and more organized user interface.

**Cons:**

- **Screen Real Estate**: Depending on the number of tabs, the tab header section can consume significant screen space.
- **Complexity**: Managing a large number of tabs can become cumbersome if not handled properly.

---

## Option 2: `st.expander`

**Description:**
`st.expander` allows sections of content to be collapsed or expanded by the user. This approach enables the application to present data in a more space-efficient manner, with users only expanding sections of interest.

**Pros:**

- **Space Efficiency**: Allows the user to collapse sections that are not immediately needed, conserving screen space.
- **User Control**: Users can control what content to view, reducing potential information overload.
- **Simple Layout**: Easy to implement and maintain within the application code.

**Cons:**

- **Slower Interaction**: Content within expanders is typically loaded or rendered upon expansion, which can lead to slower interaction when the user expands a section.
- **Less Suitable for Comparison**: It is more challenging to compare data across different sections, as expanders require users to open and close multiple sections sequentially.

---

## Decision

**We have decided to use `st.tabs` for displaying model data in our Streamlit application due to its faster display capabilities and superior user experience for quick comparisons.**

---

## Rationale

- **Faster Display**: With `st.tabs`, all the content is loaded simultaneously, allowing users to switch between different model outputs or data views without any delay. This improves the overall responsiveness of the application.
- **User Experience**: The use of tabs makes it easier for users to navigate between different sections of data. This is particularly important when users need to compare outputs from different models quickly.
- **Visual Organization**: Tabs provide a clean and organized interface, reducing the need for excessive scrolling and creating a more focused user experience.

---

## Consequences

- **Screen Real Estate**: We acknowledge that using multiple tabs might consume more screen space, particularly if there are many tabs. However, the trade-off is justified by the improved user experience and faster interaction.
- **Complexity in Management**: While managing a large number of tabs could become complex, we will mitigate this by carefully organizing the data and potentially grouping related tabs together.

---

**Status:**  
*Accepted*

---

This ADR will be revisited if user feedback indicates that the chosen approach does not meet their needs or if the application's requirements change significantly.
