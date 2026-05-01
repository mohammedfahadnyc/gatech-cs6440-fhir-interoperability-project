# Lab Setup Guide: CS 6440 FHIR RAG Assignment

## Understanding Python Dependencies for Healthcare Informatics ML Projects

### What Are Dependencies?
Dependencies are external libraries and packages that your Python program needs to run. Think of them like ingredients in a recipe - your code won't work without the right "ingredients" (packages) in the right versions.

### Why Dependencies Matter for Healthcare AI/RAG Projects
Healthcare informatics projects like our FHIR RAG system require:
- **Heavy computational libraries** (PyTorch for neural networks like Flan-T5)
- **Healthcare data processing** (FHIR resource parsing)
- **Vector databases** (ChromaDB for clinical note embeddings)
- **Hardware-specific optimizations** (CPU vs GPU, different chip architectures)  
- **Complex interdependencies** (Package A needs Package B version X, but Package C needs Package B version Y)

---

## Our FHIR RAG Project Dependencies Explained

### Core ML & Embeddings (for Flan-T5 and sentence embeddings)
```
torch>=2.2          # Neural network framework for Flan-T5 model
transformers>=4.41  # Pre-trained language models (Flan-T5, BERT, etc.)
sentence-transformers>=2.4  # Sentence embedding models for clinical notes
einops>=0.8         # Tensor operations made easy
```

### Vector Database & Retrieval (for clinical notes storage)
```
langchain==0.3.25           # RAG framework for FHIR data processing
langchain-community==0.3.24 # Community extensions
chromadb>=0.4.25           # Vector database for storing clinical note embeddings
```

### API & Utilities
```
fastapi>=0.111              # Web API framework
typing_extensions>=4.11     # Enhanced type hints
matplotlib>=3.8             # Plotting and visualization for evaluation
```

### Evaluation Tools (for comparing Flan-T5 vs GPT-3.5 answers)
```
nltk>=3.8           # Natural language processing toolkit
rouge==1.0.1        # Text summarization evaluation metrics
bert-score>=0.3.13  # Semantic similarity evaluation between answers
```

### Optional Reference Model
```
openai>=1.14               # For accessing GPT-3.5 reference answers
langchain-huggingface>=0.0.5  # HuggingFace integration
```

---

## The Hardware Challenge in Healthcare AI

### Why One Requirements File Doesn't Work for Everyone

**Different Operating Systems:**
- Windows, macOS, Linux have different binary packages for healthcare ML libraries
- Package managers handle FHIR processing dependencies differently

**Different CPU Architectures:**
- Intel x86_64 (older Macs, most PCs)
- Apple Silicon M1/M2/M3 (newer Macs)
- ARM processors (some newer laptops)

**Memory Limitations for Clinical AI:**
- Flan-T5 model loading requires significant RAM (2-4GB minimum)
- Clinical note embeddings add memory overhead (1-2GB)
- 9 patient bundles with full FHIR resources need processing power
- ChromaDB vector storage requires additional memory

### Specific Platform Challenges

**Mac Intel (x86_64):**
- PyTorch 2.3+ not available for Intel macOS
- Must use `torch==2.2.2` for stability with Flan-T5
- NumPy 2.x breaks compatibility - requires `numpy<2.0`
- Python 3.13 not supported - use Python 3.10 or 3.9

**Mac Apple Silicon (M1/M2/M3):**
- Needs ARM64-compatible packages for healthcare ML libraries
- Some FHIR processing packages may need compilation from source

**Windows:**
- CUDA support varies by PyTorch version for GPU-accelerated inference
- Some packages need Microsoft Visual C++ Build Tools

**Linux:**
- Generally best compatibility for healthcare AI workloads
- Easy CUDA setup for GPU-accelerated Flan-T5 inference

---

## Setup Options for CS 6440 Students

We provide **two tested setup options** for this assignment:

### Option 1: Google Colab (Recommended - 100% Success Rate)

**Why we recommend this:**
- ✅ Pre-installed ML packages including transformers for Flan-T5
- ✅ Free GPU access for faster clinical question answering
- ✅ No local setup required for FHIR processing
- ✅ Consistent environment for all students
- ✅ Handles 9 patient bundles without memory issues
- ✅ **Guaranteed to work** - we've tested extensively

**Quick Setup Steps:**
1. Download the assignment repository
2. Open `experiments.ipynb` in Google Colab
3. Connect to CPU runtime (or GPU if available)
4. Upload `Lab-5-FHIR-RAG-Integration.zip` to Colab
5. Follow the notebook steps:
   ```python
   # Unzip the data
   !unzip Lab-5-FHIR-RAG-Integration.zip
   
   # Install dependencies - may restart session (this is normal)
   !pip install -r requirements_google_colab.txt
   
   # If session restarts, just run the install command again
   !pip install -r requirements_google_colab.txt
   ```

**Notes:**
- Session may restart during installation - this is normal
- Simply re-run the pip install command after restart
- **Important:** For experiments or experiment1, please restart session after pip install in Colab - this is definitely recommended
- **Good practice:** Restart session after each experiment to allow your Colab to have more resources
- All dependencies are optimized for Colab environment

### Option 2: Local Development on Mac Intel (Advanced Users)

**Prerequisites:**
- macOS with Intel processor
- 32GB+ RAM recommended for full experiments
- [Homebrew](https://brew.sh) installed
- Internet connection for model downloads

**Tested Configuration:**
- ✅ Mac Intel with 64GB RAM
- ✅ Python 3.10.13 via pyenv
- ✅ PyTorch 2.2.2 (Intel-compatible version)
- ✅ All 9 patient bundles processed successfully

**Step-by-Step Setup:**

1. **Install pyenv and Python 3.10:**
   ```bash
   brew install pyenv
   pyenv install 3.10.13
   ```

2. **Configure shell integration in `~/.zshrc`:**
   ```bash
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init -)"
   ```

3. **Reload terminal:**
   ```bash
   source ~/.zshrc
   ```

4. **Create and activate virtual environment:**
   ```bash
   pyenv shell 3.10.13
   python -m venv venv310
   source venv310/bin/activate
   ```

5. **Install platform-specific requirements:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements_local_mac_intel.txt
   ```

6. **Handle potential issues:**
   ```bash
   # If you encounter NumPy or PyTorch compatibility issues:
   pip install "torch==2.2.2" "numpy<2.0"
   ```

7. **Run the experiment:**
   ```bash
   python experiments_local.py
   ```

**Important Notes for Mac Intel:**
- **PyTorch 2.3+** is not available for Intel macOS — use `torch==2.2.2`
- **Python 3.13 is not supported** — use Python 3.10 or 3.9
- **NumPy 2.x breaks compatibility** with many compiled modules — use `numpy<2.0`
- **LangChain deprecations** may show warnings; they can be resolved by updating imports later
- First run may take several minutes to download model weights (~1GB)

**Cleanup (if needed):**
```bash
# Remove environment
deactivate
rm -rf venv310

# Uninstall Python version
pyenv uninstall 3.10.13
```

---

## Requirements Files Reference

### `requirements_google_colab.txt`
- Optimized for Google Colab environment
- Includes all necessary packages for FHIR RAG processing
- Handles dependency conflicts automatically
- **100% success rate** in our testing

### `requirements_local_mac_intel.txt`
- Specifically tested on Mac Intel with 64GB RAM
- Uses PyTorch 2.2.2 for Intel compatibility
- Includes NumPy version constraints
- Platform-specific package versions

---

## Troubleshooting Common Issues

### Memory Errors During FHIR Processing
**Problem:** System freezing or out of memory errors when loading patient data
**Solutions:**
- Close other applications to free up memory
- Use Google Colab with more available memory
- Restart your Python kernel/runtime and try again

### Package Installation Conflicts
**Problem:** `pip` reports dependency conflicts between FHIR and ML packages
**Solutions:**
- Use our tested requirements files exactly as provided
- Create fresh virtual environment if mixing installations
- For Mac Intel: enforce specific versions as documented

### Model Loading Issues
**Problem:** Flan-T5 or embedding models fail to load
**Solutions:**
- Ensure sufficient internet bandwidth for initial model download
- Check available disk space (models require ~1GB)
- Use Google Colab if local resources are insufficient

### Session Restarts in Colab
**Problem:** Colab session restarts during package installation
**Solutions:**
- This is normal behavior when installing large ML packages
- Simply re-run the installation command after restart
- **For experiments:** Restart session after pip install - this is definitely recommended
- **Best practice:** Restart session after each experiment to free up memory and resources
- Continue with the notebook steps

---

## Our Recommendations

### For All Students: Start with Google Colab
1. **Primary recommendation:** Use Google Colab with `requirements_google_colab.txt`
2. **Fallback option:** Local Mac Intel setup if you have the hardware and enjoy troubleshooting
3. **Not recommended:** Other local setups unless you're experienced with ML environment management

### Success Priority
1. **Google Colab** - Guaranteed to work, focus on learning healthcare AI concepts
2. **Mac Intel Local** - If you have 16GB+ RAM and want local development experience
3. **Other platforms** - Use at your own risk, with Colab as backup

---

## Assignment-Specific Considerations

### What This Setup Enables
- **FHIR Resource Processing:** Extract clinical notes from 9 patient bundles
- **Vector Database:** Store clinical notes in ChromaDB for retrieval
- **Clinical Question Answering:** Use Flan-T5 to answer 10 specific healthcare questions
- **Evaluation:** Compare Flan-T5 answers against GPT-3.5 reference answers
- **Healthcare AI Metrics:** ROUGE and BERT-score evaluation for clinical accuracy

### Critical Success Factors
- **Model Loading:** Flan-T5 must load successfully for clinical inference
- **Vector Storage:** ChromaDB must handle clinical note embeddings
- **Memory Management:** System must handle 9 patient bundles simultaneously
- **Evaluation Pipeline:** ROUGE and BERT-score must compute successfully

---

## Final Advice for CS 6440 Students

### Do This ✅
- **Start with Google Colab** - it's tested and guaranteed to work
- Test the setup with sample data before the assignment deadline
- Focus on understanding healthcare AI concepts, not setup debugging
- Keep assignment files organized and backed up

### Avoid This ❌
- Don't spend more than 30 minutes on local setup issues
- Don't modify the assignment code structure (auto-graded)
- Don't ignore system memory warnings when processing patient data
- Don't attempt untested platform configurations close to deadlines

### Remember: Healthcare AI Focus
The goal is learning about RAG systems in healthcare informatics:
- How clinical notes can be vectorized and retrieved
- How Flan-T5 performs on healthcare question answering
- How to evaluate clinical AI system quality
- Understanding FHIR data processing workflows

**Bottom Line:** Use Google Colab unless you specifically want to learn local ML environment setup. Focus your energy on the fascinating world of healthcare AI and FHIR data processing! 🏥🤖

---

## Assignment Success Checklist

Before starting your FHIR RAG experiments:
- [ ] Environment setup complete (Colab recommended)
- [ ] Can load and run Flan-T5 model
- [ ] Can process FHIR patient bundles
- [ ] ChromaDB stores and retrieves clinical notes
- [ ] Evaluation metrics (ROUGE, BERT-score) compute correctly
- [ ] System handles all 9 patient bundles without issues

**You're ready to explore healthcare AI with FHIR data!**