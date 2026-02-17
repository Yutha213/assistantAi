# 🛡️ Expert - Your Occupational Health and Safety AI Consultant

This is a Python-based AI assistant specialized in **Occupational Health and Safety (OHS)**, capable of:

- 🔍 **Safety Information Search** - Research safety regulations, best practices, and guidelines
- 🌤️ **Weather Monitoring** - Check weather conditions for outdoor work safety
- 📨 **Safety Communications** - Send safety alerts and incident reports via email
- 📷 **Visual Safety Inspections** - Analyze workplace hazards through camera (Web app)
- 🗣️ **Multilingual Voice Support** - Communicate in 7+ languages
- 💬 **Safety Consultations** - Expert guidance on OHS matters (Web app)

## 🌍 Multilingual Support

Expert can communicate fluently in:
- **English**
- **Arabic** (العربية)
- **Hindi** (हिन्दी)
- **Urdu** (اردو)
- **Bengali** (বাংলা)
- **Nepali** (नेपाली)
- **Tagalog** (Filipino)

## 🎯 OHS Expertise

Expert provides professional guidance on:
- Risk Assessment & Hazard Identification
- Safety Regulations (OSHA, ISO 45001)
- Incident Investigation
- PPE Requirements
- Emergency Response Procedures
- Workplace Safety Audits
- Safety Training Programs
- Chemical Safety & SDS
- Ergonomics & Wellness
- Construction & Industrial Safety

---

## 🚀 Setup Instructions

This agent uses LiveKit that is 100% free!

### Prerequisites
Before you start, **make sure to follow this tutorial to set up the voice agent correctly**:  
🎥 [Watch here](https://youtu.be/An4NwL8QSQ4?si=v1dNDDonmpCG1Els)

### Installation Steps

1. **Create the Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   
   In the `.env` file, add your API keys:
   - `LIVEKIT_URL` - Your LiveKit server URL
   - `LIVEKIT_API_KEY` - Your LiveKit API key
   - `LIVEKIT_API_SECRET` - Your LiveKit API secret
   - `GOOGLE_API_KEY` - Your Google API key for the AI model
   - `GMAIL_USER` - (Optional) Your Gmail address for email functionality
   - `GMAIL_APP_PASSWORD` - (Optional) Your Gmail app password

5. **Run the Agent**
   ```bash
   python agent.py start
   ```

6. **Connect to Expert**
   
   Once running, connect to your LiveKit room using the web interface or LiveKit client to start consulting with Expert!

---

## 📋 Use Cases

- **Safety Inspections** - Get guidance on conducting workplace safety audits
- **Incident Reporting** - Assistance with incident documentation and investigation
- **Compliance Checks** - Verify compliance with safety regulations
- **Training Support** - Get safety training content and materials
- **Risk Assessments** - Conduct comprehensive risk assessments
- **Emergency Planning** - Develop emergency response procedures
- **Multilingual Safety Communication** - Communicate safety information to diverse workforces

---

## 🔧 Technical Details

- **Framework**: LiveKit Agents
- **AI Model**: Google Realtime API (Aoede voice)
- **Languages**: Python 3.10+
- **Voice**: Multilingual support with automatic language detection

---

## 🌐 Deployment

### Frontend (Vercel)
The web HUD is ready for one-click deployment to Vercel.
1. Push your code to GitHub.
2. Connect your repository to [Vercel](https://vercel.com).
3. Add the following **Environment Variables** in the Vercel dashboard:
   - `LIVEKIT_URL`
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`
   - `GOOGLE_API_KEY`

### Backend (AI Agent)
The Python-based AI agent (`agent.py`) needs to run as a long-running process (not a serverless function).
- **Host**: Use a VPS (DigitalOcean, AWS) or a specialized service like **Fly.io** or **Railway**.
- **Run Command**: `python agent.py start` (ensure the virtual environment is active).

## 📞 Support

For technical support or questions about Expert, refer to the LiveKit documentation or the tutorial video linked above.

**Stay Safe! 🛡️**
