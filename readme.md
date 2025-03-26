# Hotel Booking Analytics and Q&A System

## Overview
The **Hotel Booking Analytics and Q&A System** is designed to process and analyze hotel booking data. It provides insights into various aspects of the data, such as revenue trends, cancellation rates, geographical distribution, and lead time distribution. Additionally, the system incorporates a **Retrieval-Augmented Question Answering (RAG)** system to allow users to query the database and receive accurate answers to booking-related questions.

This project includes an **API** that facilitates querying the data, as well as a **Streamlit dashboard** for visualizing the analytics.

## Features
1. **Data Collection & Preprocessing**:
   - Uses a sample hotel booking dataset (available in CSV format) to create a MySQL database.
   - Handles data preprocessing tasks such as cleaning missing values, normalizing data, and ensuring data consistency.

2. **Analytics & Reporting**:
   The system generates the following reports:
   - **Revenue Trends Over Time**: Visualizes daily revenue over a specified period.
   - **Cancellation Rate**: Calculates the percentage of bookings that were canceled.
   - **Geographical Distribution**: Shows the distribution of bookings across different countries.
   - **Booking Lead Time Distribution**: Displays the distribution of lead times between the booking and the check-in date.

3. **Retrieval-Augmented Question Answering (RAG)**:
   - Integrates an LLM (such as Google Gemini.) with a vector database (ChromaDB) to enable natural language querying.
   - Example queries include:
     - "Show me total revenue for July 2017."
     - "Which locations had the highest booking cancellations?"
     - "What is the average price of a hotel booking?"

4. **API Development**:
   - The system exposes an API built using **FastAPI**, with the following endpoints:
     - `POST /analytics`: Returns analytics reports (e.g., revenue trends, cancellation rates).
     - `POST /ask`: Accepts a natural language question and returns an answer based on the dataset.

5. **Performance Evaluation**:
   - The accuracy of the Q&A responses is evaluated.
   - The API's response time is measured, and optimizations are applied to improve performance.

6. **Deployment & Submission**:
   - This repository includes the entire codebase, including LLM integration, analytics, and the FastAPI server.
   - Sample test queries and their expected answers.
   - A report explaining the implementation choices, challenges faced, and solutions.

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- A MySQL database or equivalent relational database for storing the hotel booking data
- Google API Key for LLM usage

### Steps to Set Up

1. **Clone the repository**:

2. **Set up a virtual environment**:
- Create a new virtual environment:
  ```
  python3 -m venv venv
  ```
- Activate the virtual environment:
  - On Linux/macOS:
    ```
    source venv/bin/activate
    ```
  - On Windows:
    ```
    venv\Scripts\activate
    ```

3. **Install dependencies**:
- Install the required packages using `pip`:
  ```
  pip install -r requirements.txt
  ```

4. **Set up the `.env` file**:
- Create a `.env` file in the root directory of the project, and add the following variables:
  ```
  DB_HOST=localhost
  DB_NAME=hotel_bookings
  DB_USER=root
  DB_PASSWORD=yourpassword
  DB_PORT=3306
  GOOGLE_APIKEY="your_google_api_key"
  ```

5. **Import Data into MySQL Database**:
- Ensure you have the correct CSV file (`hotel_bookings.csv`) in the project directory.
- The `preprocess.py` script will clean and import the CSV data into MySQL:
  ```
  python preprocess.py
  ```

6. **Run the API**:
- Start the FastAPI server:
  ```
  uvicorn api:app --reload
  ```

7. **Run the Streamlit dashboard**:
- Start the Streamlit application:
  ```
  streamlit run app.py
  ```

## Example Queries

Once the system is up and running, you can ask natural language questions about the hotel booking data. Some examples include:

- **Revenue-related queries**:
- "What is the total revenue for July 2017?"
- "Show me daily revenue for the last month."

- **Cancellation-related queries**:
- "What is the cancellation rate?"
- "Which country has the highest cancellation rate?"

- **Booking lead time queries**:
- "Show the distribution of lead times."
- "What is the average booking lead time?"

- **Geographical distribution queries**:
- "Which countries have the most bookings?"
- "Show me bookings by country."

## API Endpoints

### POST /analytics
- **Description**: Returns analytics reports, including revenue trends, cancellation rates, etc.
- **Request body**: None.
- **Response**: A JSON object with analytics data.

### POST /ask
- **Description**: Accepts a natural language question and returns an answer from the dataset.
- **Request body**:
```json
{
 "question": "What is the total revenue for July 2015?"
}
{
  "response": {
    "llm_response": "The total revenue for July 2017 was  $271,588.06.",
    "image": null
  }
{
 "question": "What is the  average price of hotel booking for  July 2015?"
}
{
  "response": {
    "llm_response": "The total revenue for July 2017 was  $97.83.",
    "image": null
  }
}
