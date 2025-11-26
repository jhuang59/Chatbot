# Prompt Management Guide

## Overview

The chatbot now supports multiple system prompts that define the chatbot's personality and behavior. You can easily switch between different prompts or create your own.

## Available Prompts

The chatbot comes with 5 pre-configured prompts:

1. **default** - General helpful assistant
   - Conversational and friendly
   - Best for general questions
   - Well-balanced approach

2. **technical_expert** - Technical knowledge expert
   - Deep technical knowledge
   - Provides code examples
   - Discusses best practices
   - Good for coding and technical questions

3. **creative_writer** - Creative writing assistant
   - Helps develop creative ideas
   - Suggests writing improvements
   - Encourages creative thinking
   - Perfect for storytelling and content creation

4. **teacher** - Educational assistant
   - Explains concepts clearly
   - Breaks down complex topics
   - Uses examples and analogies
   - Great for learning and education

5. **business_consultant** - Business strategy advisor
   - Provides strategic business advice
   - Analyzes challenges and opportunities
   - Considers business impact
   - Ideal for business discussions

## How to Change the Prompt

### Method 1: Environment Variable (Recommended for Production)

Edit your `.env` file and set `CHATBOT_PROMPT`:

```env
CHATBOT_PROMPT=technical_expert
```

Available values:
- `default` (default)
- `technical_expert`
- `creative_writer`
- `teacher`
- `business_consultant`

Then restart Docker:

```bash
sudo docker compose down
sudo docker compose up -d
```

### Method 2: View Available Prompts

To see all available prompts in code:

```bash
cat backend/app/prompts.py
```

## How to Create Custom Prompts

### Step 1: Edit `backend/app/prompts.py`

Open the file:

```bash
nano backend/app/prompts.py
```

### Step 2: Add Your Prompt

Add a new constant with your custom prompt:

```python
MY_CUSTOM_PROMPT = """You are a helpful chatbot specialized in your specific domain.

Your characteristics:
- What you should do
- How you should behave
- Your tone and style
- Any special instructions"""
```

### Step 3: Add to Available Prompts

Find the `list_available_prompts()` function and add your prompt name:

```python
def list_available_prompts() -> list:
    """Return list of available prompt names"""
    return [
        "default",
        "technical_expert",
        "creative_writer",
        "teacher",
        "business_consultant",
        "my_custom_prompt"  # Add this
    ]
```

### Step 4: Add to Prompt Dictionary

Find the `get_system_prompt()` function and add your prompt:

```python
def get_system_prompt(prompt_name: str = "default") -> str:
    prompts = {
        "default": DEFAULT_SYSTEM_PROMPT,
        "technical_expert": TECHNICAL_EXPERT_PROMPT,
        "creative_writer": CREATIVE_WRITER_PROMPT,
        "teacher": TEACHER_PROMPT,
        "business_consultant": BUSINESS_CONSULTANT_PROMPT,
        "my_custom_prompt": MY_CUSTOM_PROMPT,  # Add this
    }
    return prompts.get(prompt_name, DEFAULT_SYSTEM_PROMPT)
```

### Step 5: Use Your Custom Prompt

Set in `.env`:

```env
CHATBOT_PROMPT=my_custom_prompt
```

### Step 6: Commit Changes

```bash
git add backend/app/prompts.py .env
git commit -m "Add custom prompt: my_custom_prompt"
git push
```

## Example: Create a Customer Support Bot

```python
CUSTOMER_SUPPORT_PROMPT = """You are a professional customer support representative.

Your characteristics:
- Be empathetic and understanding
- Provide clear, helpful solutions
- Ask clarifying questions if needed
- Stay professional and courteous
- Offer to escalate to human support if needed
- Keep responses concise but thorough

When a customer has an issue:
1. Acknowledge their concern
2. Understand the problem
3. Provide a solution
4. Confirm the issue is resolved"""
```

Then add to the dictionary:

```python
"customer_support": CUSTOMER_SUPPORT_PROMPT
```

And use:

```env
CHATBOT_PROMPT=customer_support
```

## Example: Create a Code Reviewer Bot

```python
CODE_REVIEWER_PROMPT = """You are an expert code reviewer with knowledge of best practices.

Your characteristics:
- Review code for quality, security, and performance
- Suggest improvements with explanations
- Reference relevant design patterns
- Explain why changes matter
- Be constructive and educational
- Include specific examples in your reviews

When reviewing code:
1. Check for bugs and logical errors
2. Evaluate code style and readability
3. Consider performance implications
4. Review security practices
5. Suggest refactoring opportunities"""
```

## Tips for Writing Good Prompts

1. **Be Specific** - Define the exact role and responsibilities
2. **Set Tone** - Describe how the chatbot should communicate
3. **Give Context** - Explain what domain or topic the bot handles
4. **Set Boundaries** - Describe limitations and when to escalate
5. **Use Examples** - Include examples of expected behavior
6. **Be Clear** - Use simple, unambiguous language
7. **Test Thoroughly** - Try different prompts and refine based on results

## Testing Your Prompts

### Quick Test

1. Set your prompt in `.env`
2. Restart Docker: `sudo docker compose down && sudo docker compose up -d`
3. Open http://localhost:3000
4. Ask relevant questions to test the behavior
5. Compare responses with other prompts

### A/B Testing

Create two different prompts and test them with the same questions to see which works better:

```bash
# Test prompt 1
CHATBOT_PROMPT=prompt_1
# Ask questions...

# Test prompt 2
CHATBOT_PROMPT=prompt_2
# Ask the same questions...

# Compare results
```

## API Usage

You can also check which prompt is loaded via the API (add endpoint if needed):

The system uses the prompt from the environment variable, so to verify:

```bash
docker-compose logs backend | grep "CHATBOT_PROMPT"
```

## Advanced: Dynamic Prompt Selection

To allow users to select prompts via API (future enhancement):

1. Add `prompt_name` parameter to `/api/chat/conversations`
2. Store prompt choice in Conversation model
3. Use stored prompt when generating responses

Example implementation would look like:

```python
@router.post("/conversations")
def create_conversation(
    req: ConversationCreate,
    db: Session = Depends(get_db)
):
    conversation = Conversation(
        id=str(uuid.uuid4()),
        title=req.title,
        prompt_name=req.prompt_name or "default"  # Store prompt choice
    )
    db.add(conversation)
    db.commit()
```

## Troubleshooting

### Prompt Not Changing

1. Check `.env` file exists and has correct variable
2. Restart Docker containers: `sudo docker compose down && sudo docker compose up -d`
3. Check Docker logs: `sudo docker compose logs backend`
4. Verify syntax in `prompts.py`

### Prompt Not Found

1. Check spelling of prompt name in `.env`
2. Verify prompt is added to `get_system_prompt()` dictionary
3. Check it's in `list_available_prompts()` list

### Chatbot Behavior Not Changing

1. Make sure `CHATBOT_PROMPT` is set in `.env`
2. Restart Docker (changes require container restart)
3. Try with a very different prompt (e.g., switch to "technical_expert")
4. Check that prompt content is actually different

## Best Practices

1. **Keep Prompts Focused** - Each prompt should have a clear, single purpose
2. **Version Control** - Commit prompt changes to git
3. **Document Changes** - Add comments explaining prompt purpose
4. **Test Thoroughly** - Always test new prompts before deploying
5. **Collect Feedback** - See how users interact with different prompts
6. **Iterate** - Refine prompts based on real usage

## File Locations

- **Prompt Templates**: `backend/app/prompts.py`
- **Configuration**: `.env` or `backend/.env.example`
- **API Integration**: `backend/app/api/chat.py`
- **LLM Usage**: `backend/app/llm/provider.py`
