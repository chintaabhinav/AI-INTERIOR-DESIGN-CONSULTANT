# 🏠 AI Interior Design Consultant

## ✨ What It Does

Ever wondered how professional interior designers create cohesive spaces? This AI system replicates that process using multiple specialized agents:

- 📐 **Analyzes your space** - Understands dimensions, layout constraints, and flow
- 🎨 **Defines your style** - Translates preferences into concrete design direction
- 🛋️ **Recommends furniture** - Suggests specific pieces with dimensions and prices
- 💰 **Optimizes budget** - Keeps everything within your budget constraints
- 📋 **Generates complete plans** - Delivers professional design documentation

**Input:** Room details + Style preferences + Budget  
**Output:** Complete interior design plan ready to implement

---

**Sample Output:**
```
✅ 15' × 12' Living Room Design
✅ Modern Scandinavian Style
✅ Complete furniture list with 8 items
✅ Budget: $3,847 (within $4,000 target)
✅ Layout recommendations
✅ Implementation timeline
```

---

## 🛠️ Built With

- **[CrewAI](https://github.com/joaomdmoura/crewAI)** - Multi-agent orchestration framework
- **[Llama 3.3 70B](https://www.llama.com/)** - Large language model (via Groq)
- **[Streamlit](https://streamlit.io/)** - Web interface
- **Python 3.12** - Core implementation

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.12+
pip
```

### Installation
```bash
# Clone the repo
git clone https://github.com/yourusername/interior-design-agent.git
cd interior-design-agent

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Get API Keys (Free)

1. **Groq API** (for LLM): https://console.groq.com/
2. **Serper API** (for web search): https://serper.dev/

Add to `.env`:
```bash
GROQ_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

### Run
```bash
# Web interface (recommended)
streamlit run frontend/app.py

# Command line
python src/main.py
```

Open http://localhost:8501 in your browser 🎉

---

## 💡 How It Works

### Multi-Agent Architecture
```mermaid
graph TD
    A[User Input] --> B[Controller Agent]
    B --> C[Space Analysis Agent]
    C --> D[Style Consultant Agent]
    D --> E[Furniture Specialist Agent]
    E --> F[Budget Optimizer Agent]
    F --> B
    B --> G[Design Plan Output]
```

**The Team:**

| Agent | Role | Tools |
|-------|------|-------|
| 🎯 **Controller** | Orchestrates workflow | Web Search |
| 🏗️ **Space Analyst** | Validates dimensions | Custom Layout Tool |
| 🎨 **Style Consultant** | Defines aesthetics | Web Search, Scraper |
| 🛋️ **Furniture Specialist** | Finds products | Web Search, Scraper |
| 💰 **Budget Optimizer** | Manages costs | Web Search |

### Custom Tool: Room Layout Optimizer

Built a specialized tool that validates furniture placement:
```python
# Checks if furniture physically fits
# Validates clearances (30-36" walkways)
# Calculates space utilization
# Provides layout recommendations
```

**Example:**
```json
{
  "layout_valid": true,
  "open_space_percent": 75.52,
  "circulation_rating": "Excellent - Very spacious"
}
```

---

## 📋 Features

- ✅ **Multi-Agent Collaboration** - 5 specialized AI agents working together
- ✅ **Custom Tool Development** - Room layout validation with industry standards
- ✅ **Real-Time Processing** - See agents working in real-time
- ✅ **Professional Output** - Design plans ready for implementation
- ✅ **Budget Optimization** - Smart cost allocation and alternatives
- ✅ **Web Interface** - Beautiful, user-friendly UI
- ✅ **Download Reports** - Save plans as text files

---

## 🎯 Use Cases

**For Homeowners:**
- Planning room renovations
- Furniture shopping guidance
- Budget-conscious design

**For Renters:**
- Temporary space optimization
- Removable solutions
- Cost-effective improvements

**For Design Students:**
- Learning design principles
- Portfolio development
- Quick concept generation

---

## 📁 Project Structure
```
interior-design-agent/
├── src/
│   ├── main.py              # Main orchestration
│   ├── agents.py            # Agent definitions
│   ├── tasks.py             # Task definitions
│   ├── tools/
│   │   └── room_layout_optimizer.py  # Custom tool
│   └── config/
│       └── llm_config.py    # LLM setup
├── frontend/
│   └── app.py               # Streamlit UI
├── tests/                   # Test suite
├── outputs/reports/         # Generated plans
├── requirements.txt
└── README.md
```

---

## 🧪 Testing
```bash
# Run all tests
python test_setup.py        # Verify installation
python test_custom_tool.py  # Test layout optimizer
python test_agents.py       # Test agent initialization
python test_tasks.py        # Test task definitions

# Expected output: All ✓
```

---

## 📊 Performance

- **Execution Time:** 1-3 minutes per consultation
- **Token Efficiency:** ~1,000-2,000 tokens per run
- **Success Rate:** 100% with valid inputs
- **Output Quality:** Professional-grade

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Abhinav Chinta**

- GitHub: [@chintaabhinav](https://github.com/chintaabhinav)
- LinkedIn: [AbhinavChinta](https://www.linkedin.com/in/abhinav-chinta-2617l/)

---

## ⚙️ Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key