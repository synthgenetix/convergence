# 🔥 SDK Usage Guide

This guide covers using the Convergence CLI for generating audio conversations.
Master the command-line interface to unlock the full potential of synthetic conversation generation.

## 🔥 Basic Usage

### 🔥 Generate a Conversation

```bash
python -m convergence --prompt "Two friends discussing quantum computing" \
                     --duration 10 \
                     --vibe "Enthusiastic and technical" \
                     --output output/quantum_talk.wav
```

### 🔥 With Custom Environment File

```bash
python -m convergence --prompt "AI consciousness debate" \
                     --duration 15 \
                     --env .env.production \
                     --vibe "Philosophical and deep"
```

## 🔥 Using Outlines

### 🔥 Local File Outline

```bash
python -m convergence --prompt "Technical deep dive on AI" \
                     --duration 20 \
                     --outline /path/to/outline.md \
                     --vibe "Educational and structured"
```

### 🔥 URL Outline

```bash
python -m convergence --prompt "Product review discussion" \
                     --outline https://example.com/product-outline.md \
                     --duration 15
```

### 🔥 Non-Markdown Files

Non-markdown files are automatically converted.
Convergence intelligently processes PDFs, text files, and other formats using the markitdown library:

```bash
python -m convergence --prompt "Technical documentation" \
                     --outline ./docs/spec.pdf
```

## 🔥 Pre-defined Conversations

### 🔥 Using Conversation JSON

```bash
python -m convergence --conversation ./data/conversation.json
```

### 🔥 Override Output Path

```bash
python -m convergence --conversation ./data/conversation.json \
                     --output custom_output.wav
```

## 🔥 AI Transcript Generation

### 🔥 Generate with Specific Parameters

```bash
python -m convergence --generate-transcript \
                     --prompt "Two scientists discussing quantum computing" \
                     --duration 5 \
                     --vibe "Academic and curious"
```

### 🔥 Use Defaults

```bash
python -m convergence --generate-transcript
```

### 🔥 Two-Step Process

First generate the transcript:
```bash
python -m convergence --generate-transcript --duration 3
```

Then convert to audio:
```bash
python -m convergence --conversation output/conversation_[timestamp].json
```

## 🔥 Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
The following options provide complete control over conversation generation:
| `--prompt` | `-p` | Conversation topic. | Required |
| `--duration` | `-d` | Length in minutes. | 5 |
| `--vibe` | `-v` | Conversation style. | None |
| `--output` | `-o` | Output file path. | Auto-generated |
| `--outline` | `-u` | Outline file/URL. | None |
| `--conversation` | `-c` | Pre-defined conversation JSON. | None |
| `--generate-transcript` | `-g` | Generate transcript only. | False |
| `--env` | `-e` | Environment file. | .env |

## 🔥 Tips

1. **Vibe Examples**: "Professional", "Casual", "Academic", "Enthusiastic", "Mysterious".
   The vibe parameter dramatically influences the tone and style of generated conversations.
2. **Duration**: Keep under 20 minutes for best results.
   Longer conversations may take more time to generate and process.
3. **Outlines**: Use markdown format for best compatibility.
   Structured markdown with clear headings and bullet points produces the best results.
4. **Output**: WAV format provides best quality.
   Uncompressed audio ensures the highest fidelity for your generated conversations.

## 🔥 Next Steps

- Explore [Features](FEATURES) for advanced capabilities.
  Discover all the powerful features available for creating dynamic conversations.
- See [API Usage](API_USAGE) for programmatic access.
  Integrate Convergence into your applications using the RESTful API.
- Check [Development Setup](DEV_SETUP) to contribute.
  Join the community and help build the future of synthetic conversation generation.