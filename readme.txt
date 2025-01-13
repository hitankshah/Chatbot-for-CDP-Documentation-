Chatbot for CDP Documentation - Installation and Requirements
Overview
This project provides a chatbot designed to assist users with questions related to the documentation of four major Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot retrieves relevant information from these documentations to help users easily find answers to their queries.

Requirements
To get started, ensure that you have the following installed:

Python 3.7 or higher
pip (Python package installer)
Flask
BeautifulSoup4
requests
sentence-transformers
PyTorch


Installation Steps
1. Clone the Repository
Begin by cloning the repository to your local machine:


git clone https://github.com/hitankshah/Chatbot-for-CDP-Documentation-
cd Chatbot-for-CDP-Documentation-
2. Create a Virtual Environment (Optional but Recommended)
It's best to create a virtual environment to manage dependencies:

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Upgrade pip
Ensure you have the latest version of pip:

bash
Copy code
python -m pip install --upgrade pip
4. Install Dependencies
Install all the required packages by running the following command:

bash
Copy code
pip install flask beautifulsoup4 requests sentence-transformers torch==2.4.1 torchvision==0.19.1
5. Run the Application
Start the Flask application:

bash
Copy code
python app.py
The application will be accessible at http://localhost:5000.

Configuration
Documentation URLs
The chatbot uses the following URLs to fetch documentation content:

Segment Documentation: https://segment.com/docs/?ref=nav
mParticle Documentation: https://docs.mparticle.com/
Lytics Documentation: https://docs.lytics.com/
Zeotap Documentation: https://docs.zeotap.com/home/en-us
Usage
UI Access
To interact with the chatbot, visit http://localhost:5000.

API Endpoint
You can also make POST requests to /ask with a JSON payload containing the user's query. Example:

json
Copy code
{
  "query": "How do I set up a new source in Segment?"
}
Example Queries
Here are a few examples of questions you can ask the chatbot:

"How do I set up a new source in Segment?"
"How can I create a user profile in mParticle?"
"How do I build an audience segment in Lytics?"
"How can I integrate my data with Zeotap?"
Handling Variations
The chatbot can handle variations in question phrasing and respond to both specific and general queries related to the supported CDPs.

Advanced Features
Cross-CDP Comparisons
The chatbot can compare functionalities across different CDPs. For example:

"How does Segment's audience creation process compare to Lytics'?"
Complex Queries
The chatbot supports more advanced queries on configurations and integrations.

Troubleshooting
ModuleNotFoundError: Ensure all dependencies are correctly installed. You may need to reinstall pip or the required packages.
Version Conflicts: Verify the compatibility of torch and torchvision if using different versions.
License
This project is licensed under the MIT License. See the LICENSE file for more details.
