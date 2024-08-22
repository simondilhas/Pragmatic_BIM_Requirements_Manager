# Architectural Decision Record (ADR)

**ADR Title:** Choosing Between Streamlit and Flask for Building a Data-Driven Web Application

**Date:** August 14, 2024

---

## Context

We develop a open source solution to easily define and communicate BIM requirments

- **Ease of development**: We need to quickly prototype and deploy the application.
- **Interactivity**: The application should allow for dynamic updates and interactions with data visualizations.
- **Performance**: The application must efficiently handle data and respond to user inputs without significant lag.
- **Deployment**: The application should be easy to deploy and maintain, ideally with minimal setup.

Given these requirements, we evaluated two options: **Streamlit** and **Flask**.

---

## Options Considered

1. **Streamlit**
2. **Flask**

---

## Option 1: Streamlit

**Description:**
Streamlit is an open-source Python framework specifically designed for creating data-centric applications. It allows developers to create interactive dashboards and web apps with minimal effort by using a simple, declarative API.

**Pros:**

- **Simplicity and Speed**: Streamlit's API is intuitive and designed for quick prototyping, allowing developers to build interactive applications with less boilerplate code.
- **Interactive Widgets**: Built-in support for widgets like sliders, text inputs, and buttons, which simplifies adding interactivity to visualizations.
- **Real-time Updates**: Streamlit automatically handles UI updates in response to user interactions, which is critical for data exploration tools.
- **Integration with Data Libraries**: Seamless integration with popular Python data libraries such as Pandas, NumPy, and Matplotlib.
- **Deployment**: Easy to deploy with Streamlit Cloud, Docker, or any cloud platform, with minimal configuration.

**Cons:**

- **Customization**: Limited flexibility compared to Flask. Streamlit is opinionated and may not be suitable for highly customized web applications.
- **Scalability**: Streamlit is not as robust as Flask for handling large-scale applications or those requiring complex backend processing.

---

## Option 2: Flask

**Description:**
Flask is a lightweight WSGI web application framework in Python. It is more general-purpose and allows for building a wide range of web applications, from simple to complex.

**Pros:**

- **Flexibility**: Flask is highly flexible and can be used to build any type of web application, not just data-driven ones.
- **Extensibility**: Flask supports a wide range of extensions for adding features such as authentication, databases, and more.
- **Community Support**: Flask has a large and active community, providing a wealth of resources, plugins, and tutorials.

**Cons:**

- **Development Speed**: Requires more boilerplate code compared to Streamlit, especially for data-centric applications.
- **Interactivity**: Adding dynamic features and real-time updates requires additional work, often involving JavaScript, AJAX, or WebSockets.
- **Learning Curve**: Flask may require more effort to learn and implement for developers primarily focused on data science rather than web development.

---

## Decision

**We have decided to use Streamlit for the development of our data-driven web application.**

---

## Rationale

- **Ease of Use**: Streamlit's simplicity and rapid development capabilities align well with our need for quick prototyping and iteration. It allows our team, which primarily consists of data scientists, to build and deploy the application without needing extensive web development expertise.
- **Interactivity**: Streamlit's built-in interactivity features are perfectly suited for the type of dynamic, data-driven visualizations we need to implement.
- **Integration**: The ability to easily integrate with Python's data libraries allows us to focus on data manipulation and visualization rather than on web infrastructure.
- **Deployment**: The simplicity of deploying Streamlit applications ensures that we can maintain and scale the application with minimal overhead.

---

## Consequences

- **Limited Customization**: We accept the trade-off of less flexibility in exchange for faster development and ease of use. For this project, the limitations in customization are not significant enough to outweigh the benefits.
- **Scalability**: While Streamlit is not as scalable as Flask for large or complex applications, it meets the current scope of our project. If the application's needs grow beyond Streamlit's capabilities, we will reconsider our options or potentially integrate Flask for more complex back-end needs.

---

**Status:**  
*Accepted*

---

This ADR will be revisited if the project's scope or requirements change significantly, necessitating a re-evaluation of our technology stack.
