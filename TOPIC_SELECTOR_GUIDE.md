# English Conversation Teacher - Topic Selector Guide

## Overview

This guide explains how to use the new topic-based conversation system with PersonaPlex. You can now select from predefined conversation topics before starting a dialogue with the AI teacher.

## What's New

### 1. **5 Conversation Topics** (Easy to Extend)
- **Self Introduction** (Beginner) — Learn to introduce yourself
- **Shopping** (Beginner) — Practice shopping conversations
- **At the Restaurant** (Beginner) — Practice dining and ordering
- **Travel & Directions** (Intermediate) — Practice travel and directions
- **Job Interview** (Intermediate) — Practice interview conversations

Each topic has a carefully crafted system prompt that guides the AI to behave as an appropriate conversation partner.

### 2. **New HTTP Endpoint**
- `GET /api/topics` — Returns JSON list of available topics

### 3. **Web UI for Topic Selection**
- Open `topic_selector.html` in your browser
- Select a topic and voice
- Start conversing with the AI teacher

## Architecture

### Backend Changes

**File: `moshi/topics.py`** (NEW)
```python
TOPICS = {
    "self_introduction": {
        "label": "Tự giới thiệu (Self Introduction)",
        "level": "Beginner",
        "description": "Learn to introduce yourself in English",
        "prompt": "You are a friendly and encouraging English conversation teacher..."
    },
    ...
}
```

Helper functions:
- `get_topic_prompt(topic_id)` — Get full system prompt for a topic
- `get_topics_list()` — Get topic metadata for UI

**File: `moshi/server.py`** (MODIFIED)
- Added `async def handle_topics(request)` (line ~90) — New endpoint
- Modified `handle_chat` (line ~170) — Now checks for `topic_id` query parameter
  - If `topic_id` is provided, uses prompt from `topics.py`
  - Otherwise falls back to `text_prompt` (backward compatible)
- Added route `app.router.add_get("/api/topics", handle_topics)` (line ~460)

### Query Parameter Support

When connecting via WebSocket, you can now use either:

**Option 1: Topic ID (NEW)**
```
ws://localhost:8998/api/chat?topic_id=shopping&voice_prompt=NATF0.pt&...
```

**Option 2: Raw Text Prompt (OLD - Still Works)**
```
ws://localhost:8998/api/chat?text_prompt=You%20are%20a%20helpful%20teacher&voice_prompt=NATF0.pt&...
```

If both are provided, `topic_id` takes precedence.

## Usage

### 1. Setup HuggingFace Access

PersonaPlex requires access to the gated model on HuggingFace. You need:

1. **Accept the model license**: https://huggingface.co/nvidia/personaplex-7b-v1
2. **Get HuggingFace token**: https://huggingface.co/settings/tokens
3. **Set environment variable**:
   ```bash
   export HF_TOKEN=<your_huggingface_token>
   ```

### 2. Start the Server

```bash
cd personaplex/moshi

# Run the server (requires GPU with 16GB+ VRAM)
SSL_DIR=$(mktemp -d)
python -m moshi.server --ssl "$SSL_DIR" --port 8998
```

The server will print:
```
Access the Web UI directly at https://localhost:8998
```

**Note**: First run will download ~7GB of model weights.

**If GPU memory is insufficient**, add `--cpu-offload`:
```bash
python -m moshi.server --ssl "$SSL_DIR" --port 8998 --cpu-offload
```

### 2. Open Topic Selector UI

In your browser, navigate to:
```
file:///path/to/personaplex/topic_selector.html
```

Or if serving locally:
```
http://localhost:8998/topic_selector.html
```

(You may need to copy `topic_selector.html` to your static content directory)

### 3. Select Topic and Voice

- Choose a conversation topic from the 5 cards
- Optionally select a voice (Natural Female, Natural Male, Varied Female, Varied Male)
- Click "Start Conversation"

### 4. Have a Conversation

Once connected:
- The AI teacher will greet you based on the selected topic
- Speak English (you'll need to add microphone handling in a real app)
- The AI responds in real-time with full-duplex audio
- Text transcript appears in real-time
- Click "Disconnect" to end the session

## Extending Topics

To add more conversation topics:

1. **Edit `moshi/topics.py`**:
```python
TOPICS = {
    ...existing topics...,
    "new_topic_id": {
        "label": "Display Name (Vietnamese + English)",
        "level": "Beginner | Intermediate | Advanced",
        "description": "Short description for UI",
        "prompt": """You are an English conversation teacher for Vietnamese learners.
Topic: New Topic. Help the student practice...
[Detailed instruction for the teacher role]"""
    },
}
```

2. **Restart the server** — Changes are auto-loaded

3. **New topic appears in UI** — Next time you fetch `/api/topics`

## Testing Without Microphone

To test the API endpoint:

```bash
# Get list of topics
curl http://localhost:8998/api/topics | jq

# Example output:
# [
#   {
#     "id": "self_introduction",
#     "label": "Tự giới thiệu (Self Introduction)",
#     "level": "Beginner",
#     "description": "Learn to introduce yourself in English"
#   },
#   ...
# ]
```

## Prompt Design Tips

When writing system prompts for new topics:

1. **Start with context**: "You are a friendly English conversation teacher for Vietnamese learners."
2. **Set the topic**: "Topic: [Topic Name]. Help the student practice: [specific skills]."
3. **Give speaking guidance**: "Speak at 70% normal speed. Use simple/intermediate vocabulary."
4. **Instruction for errors**:
   - Pronunciation: "When the student makes a pronunciation error, gently repeat the correct version naturally."
   - Grammar: "When they make a grammar mistake, model the correct form while continuing the conversation."
5. **Encouragement**: "Be supportive and ask follow-up questions."

## Backward Compatibility

The old system still works:

```bash
# Old way — still works
curl "ws://localhost:8998/api/chat?text_prompt=You%20are%20helpful&voice_prompt=NATF0.pt"

# New way — cleaner
curl "ws://localhost:8998/api/chat?topic_id=shopping&voice_prompt=NATF0.pt"
```

Both approaches will set the system prompt correctly.

## Files Changed

| File | Change | Type |
|------|--------|------|
| `moshi/topics.py` | NEW | Python module with topic definitions |
| `moshi/server.py` | MODIFIED | Added endpoint + topic_id handling |
| `topic_selector.html` | NEW | Vanilla JS UI for topic selection |

## Files Not Changed

- `moshi/models/lm.py` — No changes needed
- `moshi/modules/streaming.py` — No changes needed
- `client/` (React client) — No changes needed
- Web UI (automatic static serving) — Works as before

---

**Happy teaching! 🎓**
