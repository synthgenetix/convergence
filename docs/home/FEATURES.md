# ✨ Features

Convergence offers a rich set of features for generating synthetic audio conversations.

## Core Features

### 🧬 Neural Synthesis
Generate natural conversations on any topic with just one CLI command. The AI understands context and creates realistic dialogue flows.

### 🎭 Dynamic Personas
AI-driven personalities with distinct voices. Configure personalities through:
- **Prompt**: Define the scenario and participants.
- **Vibe**: Set the tone and style.
- **Custom Transcripts**: Use your own dialogue.
- **Outline**: Provide structured guidance.

### 📋 Outline Support
Guide conversations with structured content:
- Support for local files and URLs.
- Markdown, text, and other formats via `markitdown` conversion.
- Use as conversation spec, protocol, or guidance.
- Automatic truncation to 50KB for performance.
- Graceful fallback if processing fails.

### 🗣️ Pre-defined Conversations
Generate audio from JSON conversation transcripts:
- Create your own transcripts manually.
- Use AI-generated transcripts.
- Automatic voice assignment based on speaker gender.
- Environment variable substitution in configs.

### 📝 AI Transcript Generation
Create realistic dialogues using GPT-4.1:
- Smart dialogue generation with context awareness.
- Configurable parameters (prompt, duration, vibe).
- JSON output in standard conversation format.
- No sensitive data in generated files.

### 🎤 Real TTS Integration
OpenAI text-to-speech with automatic voice selection:
- Supports all OpenAI voices.
- Automatic voice assignment by gender:
  - Female voices: alloy, coral, fable, nova, sage.
  - Male voices: ash, ballad, echo, onyx, shimmer.
- Uses `tts-1` model for high-quality speech.
- Consistent voice throughout conversation.

### 🔮 Seamless Flow
Natural conversation progression:
- No abrupt shifts or endings.
- Context-aware responses.
- Realistic timing and pacing.
- Multi-speaker support.

### 🌐 Self-hosted, API First
RESTful API with Docker support:
- Build your own UI.
- Full self-hosting capability.
- pip package available.
- Docker deployment ready.

### 🎨 Developer-Friendly CLI
Clean, intuitive command-line experience:
- **DevEx is a priority** 🔥
- Rich help documentation.
- Aesthetic sci-fi themed interface.
- Clear error messages.

## Advanced Features

### Environment Management
- Hierarchical configuration loading.
- Support for multiple environments.
- Local overrides capability.
- Secure credential handling.

### Format Support
- Automatic file format conversion.
- URL content fetching.
- Markdown optimization.
- Bullet point standardization.

### Audio Generation
- High-quality WAV output.
- Configurable duration.
- Natural speech patterns.
- Realistic conversation flow.

### Security Features
- No hardcoded secrets.
- Input validation.
- Path security checks.
- Optional API authentication.

## Coming Soon

- Web interface for non-technical users.
- More language and accent support.
- Additional TTS providers.
- Conversation visualization tools.
- Template sharing community.

## Next Steps

- Try out examples in [SDK Usage](SDK_USAGE.md).
- Set up the API with [API Usage](API_USAGE.md).
- Learn about [Self Hosting](SELF_HOST.md) options.