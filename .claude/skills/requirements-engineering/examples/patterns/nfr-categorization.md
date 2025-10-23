### Pattern: NFR Categorization and Specification

**Description:** Non-Functional Requirements (NFRs) define the quality attributes of a system and how it performs, rather than what it does. Properly categorizing and specifying NFRs is crucial for building a robust, usable, and maintainable system. This pattern outlines common NFR categories and guidance for their specification.

**Common NFR Categories:**

1.  **Performance:**
    *   **Definition:** How quickly and efficiently the system performs its functions.
    *   **Sub-categories:** Response time, throughput, latency, resource utilization.
    *   **Example Specification:** "The system shall process 100 transactions per second with a 99% success rate and an average response time of less than 200ms."

2.  **Security:**
    *   **Definition:** The system's ability to protect information and data from unauthorized access, use, disclosure, disruption, modification, or destruction.
    *   **Sub-categories:** Authentication, authorization, data privacy, data integrity, auditability.
    *   **Example Specification:** "All user passwords shall be hashed using bcrypt with a minimum of 10 rounds and stored securely. The system shall implement multi-factor authentication for administrative access."

3.  **Usability:**
    *   **Definition:** The ease with which users can learn, operate, and understand the system.
    *   **Sub-categories:** Learnability, efficiency, memorability, error prevention, satisfaction.
    *   **Example Specification:** "New users shall be able to complete the registration process within 2 minutes without referring to help documentation. The system shall provide clear error messages for all invalid inputs."

4.  **Reliability:**
    *   **Definition:** The ability of the system to perform its required functions under stated conditions for a specified period of time.
    *   **Sub-categories:** Availability, fault tolerance, recoverability, mean time between failures (MTBF).
    *   **Example Specification:** "The system shall be available 99.9% of the time during business hours (9 AM - 5 PM EST, Monday-Friday). In case of a critical system failure, data recovery shall be completed within 4 hours."

5.  **Maintainability:**
    *   **Definition:** The ease with which the system can be modified, understood, and repaired.
    *   **Sub-categories:** Modifiability, testability, analyzability, serviceability.
    *   **Example Specification:** "The codebase shall adhere to established coding standards (e.g., PEP 8 for Python, Airbnb style guide for JavaScript) and achieve a minimum code coverage of 80% for unit tests."

6.  **Scalability:**
    *   **Definition:** The ability of the system to handle an increasing amount of work or its potential to be enlarged to accommodate that growth.
    *   **Sub-categories:** Horizontal scalability, vertical scalability, elasticity.
    *   **Example Specification:** "The system shall be able to support a 50% increase in user load within a 3-month period by adding additional server instances without requiring code changes."

7.  **Portability:**
    *   **Definition:** The ease with which the system can be transferred from one environment to another.
    *   **Sub-categories:** Adaptability, installability, replaceability.
    *   **Example Specification:** "The application shall be deployable on both AWS EC2 and Google Cloud Platform (GCP) using Docker containers with minimal configuration changes."

8.  **Sustainability / Environmental:**
    *   **Definition:** The system's impact on the environment, including energy consumption and resource usage.
    *   **Sub-categories:** Energy efficiency, carbon footprint, resource optimization.
    *   **Example Specification:** "The system's average energy consumption per transaction shall not exceed 0.01 kWh. The data centers used shall be powered by at least 75% renewable energy sources."

**Guidance for Specification:**

-   **Quantify:** Whenever possible, specify NFRs using measurable metrics (e.g., 99.9% availability, 2-second response time).
-   **Contextualize:** Define the conditions under which the NFRs must be met (e.g., "under a load of 100 concurrent users," "during business hours").
-   **Prioritize:** Use techniques like MoSCoW to prioritize NFRs, as not all NFRs can be equally critical.
-   **Traceability:** Link NFRs to architectural decisions, design choices, and test cases.
-   **Early Consideration:** NFRs should be considered early in the development lifecycle, as they often have significant architectural implications.
