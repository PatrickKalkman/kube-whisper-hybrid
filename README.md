# KubeWhisper Hybrid: Voice Control Your Kubernetes Cluster (Now More Affordable!)

![KubeWhisper Hybrid Cover](cover.jpg)

[![KubeWhisper in Action](https://img.youtube.com/vi/IaMOZ9jS8_Q/maxresdefault.jpg)](https://www.youtube.com/watch?v=IaMOZ9jS8_Q)

[![GitHub stars](https://img.shields.io/github/stars/PatrickKalkman/kube-whisper-hybrid)](https://github.com/PatrickKalkman/kube-whisper-hybrid/stargazers)
[![GitHub contributors](https://img.shields.io/github/contributors/PatrickKalkman/kube-whisper-hybrid)](https://github.com/PatrickKalkman/kube-whisper-hybrid/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/PatrickKalkman/kube-whisper-hybrid)](https://github.com/PatrickKalkman/kube-whisper-hybrid)
[![open issues](https://img.shields.io/github/issues/PatrickKalkman/kube-whisper-hybrid)](https://github.com/PatrickKalkman/kube-whisper-hybrid/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

Control your Kubernetes cluster through natural conversation - now with local speech processing and drastically reduced costs! KubeWhisper Hybrid combines local speech-to-text, affordable cloud LLMs, and high-quality voice synthesis to make voice-controlled Kubernetes accessible to everyone.

Read the full story behind KubeWhisper Hybrid in my [Medium article](https://medium.com/p/70c9345eb8c3).

## ✨ Key Features

- **Cost-Effective**: Up to 90% cheaper than the original version through hybrid architecture
- **Enhanced Privacy**: Local speech processing keeps your voice data on your machine
- **Natural Voice Control**: Talk to your cluster like you're chatting with a colleague
- **Smart Command Translation**: Automatically converts speech to the right kubectl commands
- **High-Quality Voice**: Crystal clear responses using ElevenLabs text-to-speech
- **Secure by Design**: Uses your existing kubectl credentials and permissions
- **Fully Documented API**: Easy to extend with your own custom commands

## 🏗️ Architecture

KubeWhisper Hybrid uses a three-part architecture to optimize for both cost and privacy:

1. **Local Speech-to-Text**: Uses mlx-whisper for fast, private voice transcription on your machine
2. **Cloud LLM**: Leverages DeepSeek V3 for accurate, cost-effective command understanding
3. **Voice Synthesis**: Employs ElevenLabs for natural-sounding responses

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- A configured Kubernetes cluster
- A DeepSeek API key
- An ElevenLabs API key (optional, but recommended for voice output)
- A decent microphone

### Installation

1. **Install UV** (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone & Navigate**:
```bash
git clone https://github.com/PatrickKalkman/kube-whisper-hybrid
cd kube-whisper-hybrid
```

3. **Set API Keys**:
```bash
export DEEPSEEK_API_KEY='your-deepseek-api-key-here'
export ELEVENLABS_API_KEY='your-elevenlabs-api-key-here'
```

### Usage Examples

```bash
# Text mode (direct questions)
uv run kubewhisper -t "show me all pods in default namespace"

# Voice mode
uv run kubewhisper --voice

# Voice mode with specific input device
uv run kubewhisper --voice --device <device_index>

# Voice mode with voice output
uv run kubewhisper --voice --output voice

# Verbose output
uv run kubewhisper -v --text "show all my services"
```

## 💰 Cost Comparison

- **Original Version**: $10-20 per day of regular use
- **Hybrid Version**: ~$1.50 per day + free tier ElevenLabs

## 🔒 Security

KubeWhisper Hybrid is designed with security in mind:

- Uses your existing Kubernetes RBAC permissions
- Function-based access control for commands
- Local voice processing for enhanced privacy
- No permanent storage of voice data

## 🛠️ Extending KubeWhisper

Adding new commands is simple with our decorator-based system:

```python
@FunctionRegistry.register(
    description="Get the logs from a specified pod",
    response_template="The logs from pod {pod} in namespace {namespace} are: {logs}"
)
async def get_pod_logs(pod_name: str, namespace: str = "default"):
    # Your implementation here
    pass
```

## 🤝 Contributing

We love contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔮 Future Plans

- Full local LLM support
- Custom fine-tuned models for better command recognition
- Multi-language support
- Expanded command library
- Local text-to-speech options

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI's Whisper for the original speech recognition model
- MLX team for the optimized Whisper implementation
- DeepSeek for affordable LLM API
- ElevenLabs for high-quality voice synthesis
- The Kubernetes Python client team
- All our contributors and users!

---

Built with ❤️ by the community. Star us on GitHub if you find this useful!
