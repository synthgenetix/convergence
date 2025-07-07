# 🔥 Features

Convergence offers a rich set of features for generating synthetic audio conversations.
From neural synthesis to self-hosted deployments, this platform provides everything you need for creating lifelike dialogues.

## Core Features

### 🔥 Neural Synthesis
Generate natural conversations on any topic with just one CLI command.
The AI understands context and creates realistic dialogue flows that capture the nuances of human conversation.

### 🔥 Dynamic Personas
AI-driven personalities with distinct voices. Configure personalities through:
- **Prompt**: Define the scenario and participants.
  Create detailed character descriptions and scenario setups for more engaging conversations.
- **Vibe**: Set the tone and style.
  Whether casual, professional, or philosophical, the vibe parameter shapes the entire conversation.
- **Custom Transcripts**: Use your own dialogue.
  Import pre-written scripts or conversations to generate audio with specific content.
- **Outline**: Provide structured guidance.
  Guide the AI with bullet points or structured notes to ensure key topics are covered.

### 🔥 Outline Support
Guide conversations with structured content:
- Support for local files and URLs.
  Load outlines from your filesystem or directly from web resources.
- Markdown, text, and other formats via `markitdown` conversion.
  The system intelligently converts various document formats into structured guidance.
- Use as conversation spec, protocol, or guidance.
  Outlines can define strict protocols or provide flexible conversation guidelines.
- Automatic truncation to 50KB for performance.
  Large documents are intelligently trimmed to maintain optimal processing speed.
- Graceful fallback if processing fails.
  The system continues generating conversations even if outline processing encounters issues.

### 🔥 Pre-defined Conversations
Generate audio from JSON conversation transcripts:
- Create your own transcripts manually.
  Write exact dialogues in JSON format for precise control over conversations.
- Use AI-generated transcripts.
  Let the AI create transcripts that you can review and modify before generation.
- Automatic voice assignment based on speaker gender.
  The system intelligently matches voices to speakers for consistent audio output.
- Environment variable substitution in configs.
  Use environment variables in your configurations for flexible deployments.

### 🔥 AI Transcript Generation
Create realistic dialogues using GPT-4.1:
- Smart dialogue generation with context awareness.
- Configurable parameters (prompt, duration, vibe).
- JSON output in standard conversation format.
- No sensitive data in generated files.

### 🔥 Real TTS Integration
OpenAI text-to-speech with automatic voice selection:
- Supports all OpenAI voices.
  Access the full range of OpenAI's text-to-speech voice options.
- Automatic voice assignment by gender:
  - Female voices: alloy, coral, fable, nova, sage.
  - Male voices: ash, ballad, echo, onyx, shimmer.
- Uses `tts-1` model for high-quality speech.
  The latest TTS model ensures natural-sounding, expressive audio output.
- Consistent voice throughout conversation.
  Each speaker maintains the same voice throughout the entire dialogue.

### 🔥 Seamless Flow
Natural conversation progression:
- No abrupt shifts or endings.
  Conversations flow naturally from beginning to end without jarring transitions.
- Context-aware responses.
  Each response considers the full conversation history for coherent dialogue.
- Realistic timing and pacing.
  Natural pauses and speech patterns make conversations feel authentic.
- Multi-speaker support.
  Generate conversations with two or more participants seamlessly.

### 🔥 Self-hosted, API First
RESTful API with Docker support:
- Build your own UI.
  The RESTful API allows you to create custom interfaces for your specific needs.
- Full self-hosting capability.
  Run Convergence on your own infrastructure for complete control and privacy.
- pip package available.
  Easy installation through Python's package manager for quick deployment.
- Docker deployment ready.
  Container-based deployment ensures consistency across environments.

### 🔥 Developer-Friendly CLI
Clean, intuitive command-line experience:
- **DevEx is a priority** 🔥.
  Every aspect of the CLI is designed with developer experience in mind.
- Rich help documentation.
  Comprehensive help text guides you through every command and option.
- Aesthetic sci-fi themed interface.
  The cyberpunk-inspired design makes working with Convergence a visual pleasure.
- Clear error messages.
  When things go wrong, you'll know exactly what happened and how to fix it.

## Advanced Features

### 🔥 Environment Management
- Hierarchical configuration loading.
  Configuration files cascade from general to specific for maximum flexibility.
- Support for multiple environments.
  Easily switch between development, staging, and production configurations.
- Local overrides capability.
  Personal settings can override defaults without affecting team members.
- Secure credential handling.
  Sensitive data is kept secure and never exposed in logs or error messages.

### 🔥 Format Support
- Automatic file format conversion.
  The system handles various document formats seamlessly without manual conversion.
- URL content fetching.
  Pull content directly from the web for dynamic conversation generation.
- Markdown optimization.
  Markdown documents are parsed and optimized for better conversation flow.
- Bullet point standardization.
  Lists and outlines are normalized for consistent processing.

### 🔥 Audio Generation
- High-quality WAV output.
  Audio files are generated in uncompressed WAV format for maximum quality.
- Configurable duration.
  Control conversation length from quick exchanges to extended discussions.
- Natural speech patterns.
  Speech includes realistic pauses, inflections, and emotional tones.
- Realistic conversation flow.
  Conversations progress naturally with appropriate turn-taking and responses.

### 🔥 Security Features
- No hardcoded secrets.
  All sensitive data is managed through environment variables and secure storage.
- Input validation.
  User inputs are thoroughly validated to prevent injection attacks.
- Path security checks.
  File system access is restricted to prevent unauthorized file operations.
- Optional API authentication.
  Enable API key authentication for production deployments.

## Coming Soon

- Web interface for non-technical users.
  A beautiful web UI is coming to make Convergence accessible to everyone.
- More language and accent support.
  Expand beyond English to support global conversation generation.
- Additional TTS providers.
  Integration with alternative text-to-speech services for more voice options.
- Conversation visualization tools.
  Visual representations of conversation flow and structure.
- Template sharing community.
  Share and discover conversation templates with the Convergence community.

## Next Steps

- Try out examples in [SDK Usage](SDK_USAGE).
  Get hands-on with practical examples and learn all the CLI commands.
- Set up the API with [API Usage](API_USAGE).
  Build applications using the RESTful API endpoints.
- Learn about [Self Hosting](SELF_HOST) options.
  Deploy Convergence on your own infrastructure for complete control.