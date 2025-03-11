# 💬 AI Chatbot for Google Sheets with DeepSeek-R1 & Streamlit  

🚀 A smart assistant that answers questions about **Google Sheets** data in real time, using **Llama3.2 on Ollama** and **Streamlit** for a ChatGPT-like experience.

---

## 📌 **Features**  
✅ **Interactive chat** with conversation memory.  
✅ **Natural language responses** powered by AI.  
✅ **Real-time data access & analysis** from Google Sheets.  
✅ **Free & easy to use** with open-source technologies.  

---

## 🎥 **Demo**
📸 
Run the following command to generate an image:

```bash
streamlit run app.py


## ⚙️ Installation & Setup
Follow these steps to run the chatbot on your machine:

##🔹 1. Clone the repository
git clone https://github.com/WesleyG31/AI-Agent-with-custom-dataset-streamlit.git
cd AI-Agent-with-custom-dataset-streamlit

##2. Install dependencies
pip install requirements.txt

##3. Configure Google Sheets API
To allow the chatbot to access Google Sheets:

Go to Google Cloud Console.
Create a new project and enable Google Sheets API and Google Drive API.
Create a service account under "Credentials" and download the JSON key file.
Rename the file as key.json and place it in the project folder.
Share your Google Sheet with the service account email (@gserviceaccount.com).

##🚀 How to Use
Run the following command to start the chat:

streamlit run app.py


##📜 Example Usage
Example conversation with the chatbot:
👤 User: How many fraud cases are in the data?
🤖 AI: There are 57 recorded fraud cases in the spreadsheet.


##👤 User: How many fraud cases are in the data?
🤖 AI: There are 57 recorded fraud cases in the spreadsheet.

## 📂 AI-Agent-with-custom-dataset-streamlit
 ├── 📜 app.py            # Main chatbot code
 ├── 📜 key.json   # Google Sheets credentials 
 ├── 📜 requirements.txt   # List of dependencies
 ├── 📜 README.md          # Project documentation




