<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Chatbot for CDP Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 0.5em;
        }
        h2 {
            font-size: 2em;
            margin-bottom: 0.5em;
        }
        h3 {
            font-size: 1.5em;
            margin-bottom: 0.5em;
        }
        ul {
            list-style-type: disc;
            margin-left: 20px;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            max-width: 100%;
        }
        .section-title {
            font-weight: bold;
        }
        .important {
            color: red;
        }
    </style>
</head>
<body>

    <h1>Chatbot for CDP Documentation</h1>
    <p><strong>Overview:</strong></p>
    <p>This project provides a chatbot capable of answering questions related to four Customer Data Platform (CDP) documentations: Segment, mParticle, Lytics, and Zeotap. The chatbot retrieves relevant information from these documentations to assist users with their queries.</p>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.7 or higher</li>
        <li>pip (Python package installer)</li>
        <li>Flask</li>
        <li>BeautifulSoup4</li>
        <li>requests</li>
        <li>sentence-transformers</li>
        <li>PyTorch</li>
    </ul>

    <h2>Installation Steps</h2>
    <p><strong>1. Clone the Repository</strong></p>
    <pre>
git clone &lt;repository-url&gt;
cd &lt;repository-folder&gt;
    </pre>

    <p><strong>2. Create a Virtual Environment (Optional but recommended)</strong></p>
    <pre>
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
    </pre>

    <p><strong>3. Upgrade pip</strong></p>
    <pre>
python -m pip install --upgrade pip
    </pre>

    <p><strong>4. Install Dependencies</strong></p>
    <pre>
pip install flask beautifulsoup4 requests sentence-transformers torch==2.4.1 torchvision==0.19.1
    </pre>

    <p><strong>5. Run the Application</strong></p>
    <pre>
python app.py
    </pre>
    <p>The application will be accessible at <strong>http://localhost:5000</strong>.</p>

    <h2>Configuration</h2>
    <p><strong>Documentation URLs:</strong> The chatbot uses the following URLs to fetch documentation content:</p>
    <ul>
        <li>Segment Documentation: <a href="https://segment.com/docs/?ref=nav">https://segment.com/docs/?ref=nav</a></li>
        <li>mParticle Documentation: <a href="https://docs.mparticle.com/">https://docs.mparticle.com/</a></li>
        <li>Lytics Documentation: <a href="https://docs.lytics.com/">https://docs.lytics.com/</a></li>
        <li>Zeotap Documentation: <a href="https://docs.zeotap.com/home/en-us">https://docs.zeotap.com/home/en-us</a></li>
    </ul>

    <h2>Usage</h2>
    <p><strong>UI Access:</strong> Visit <a href="http://localhost:5000">http://localhost:5000</a> to interact with the chatbot.</p>
    <p><strong>API Endpoint:</strong> You can also make POST requests to /ask with a JSON payload containing the user's query.</p>

    <h3>Example Queries</h3>
    <ul>
        <li>"How do I set up a new source in Segment?"</li>
        <li>"How can I create a user profile in mParticle?"</li>
        <li>"How do I build an audience segment in Lytics?"</li>
        <li>"How can I integrate my data with Zeotap?"</li>
    </ul>

    <h2>Handling Variations</h2>
    <p>The chatbot can handle variations in question phrasing and respond to both specific and general queries related to the supported CDPs.</p>

    <h2>Advanced Features</h2>
    <ul>
        <li><strong>Cross-CDP Comparisons:</strong> The chatbot can compare functionalities across different CDPs, e.g., "How does Segment's audience creation process compare to Lytics'?"</li>
        <li><strong>Complex Queries:</strong> It supports advanced queries on configurations and integrations.</li>
    </ul>

    <h2>Troubleshooting</h2>
    <p><strong>ModuleNotFoundError:</strong> Ensure all dependencies are installed correctly. Reinstall pip or packages if necessary.</p>
    <p><strong>Version Conflicts:</strong> Verify the compatibility of torch and torchvision if using different versions.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the LICENSE file for details.</p>

</body>
</html>
