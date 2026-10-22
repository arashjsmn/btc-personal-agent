import os
from dotenv import load_dotenv
from groq import Groq

from tools.btc_analysis import get_btc_analysis
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.episodic import EpisodicMemory

import json


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

short_memory = ShortTermMemory()
long_memory = LongTermMemory()
episodic_memory = EpisodicMemory()

preference_tool = {
    "type": "function",
    "function": {
        "name": "save_user_preference",
        "description": (
            "Save a user preference to long-term memory. "
            "Use this when the user explicitly states or changes "
            "their preferences."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "enum": [
                        "risk_tolerance",
                        "investment_horizon",
                        "knowledge_level",
                        "explanation_style"
                    ],
                    "description": "The preference to update."
                },
                "value": {
                    "type": "string",
                    "description": "The user's preferred value."
                }
            },
            "required": ["key", "value"],
            "additionalProperties": False
        }
    }
}



def save_user_preference(key, value):
    allowed_values = {
        "risk_tolerance": {"low", "medium", "high"},
        "investment_horizon": {
            "short-term", "medium-term", "long-term"
        },
        "knowledge_level": {
            "beginner", "intermediate", "advanced"
        }
    }

    allowed_keys = {
        "risk_tolerance",
        "investment_horizon",
        "knowledge_level",
        "explanation_style"
    }

    if key not in allowed_keys:
        return "Error: unsupported preference."

    if not isinstance(value, str) or not value.strip():
        return "Error: value must be a non-empty string."

    value = value.strip()

    if len(value) > 100:
        return "Error: preference value is too long."

    if key in allowed_values and value.lower() not in allowed_values[key]:
        return f"Error: invalid value for {key}."
    
    print(f"TOOL CALLED: {key} = {value}", flush=True)

    long_memory.update(key, value)

    return f"Successfully saved {key} = {value}"


def record_user_feedback(feedback):
    if not isinstance(feedback, str) or not feedback.strip():
        return "Error: feedback must be a non-empty string."

    feedback = feedback.strip()

    if len(feedback) > 500:
        return "Error: feedback is too long."

    episodic_memory.add_episode(
        "user_feedback",
        feedback
    )

    print(f"FEEDBACK SAVED: {feedback}", flush=True)

    return "Feedback successfully saved to episodic memory."


feedback_tool = {
    "type": "function",
    "function": {
        "name": "record_feedback",
        "description": (
            "Save explicit user feedback about a previous response "
            "to episodic memory. Use this when the user says an "
            "explanation was too complicated, too long, unclear, "
            "or requests a specific improvement. Do not infer "
            "feedback that the user did not express."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "feedback": {
                    "type": "string",
                    "description": (
                        "A concise description of the user's "
                        "explicit feedback and requested improvement."
                    )
                }
            },
            "required": ["feedback"],
            "additionalProperties": False
        }
    }
}



def detect_user_feedback(message):
    text = message.lower()

    feedback_phrases = [
        "too complicated",
        "too long",
        "too confusing",
        "not clear",
        "hard to understand",
        "simpler",
        "shorter explanations",
        "shorter responses",
        "three short bullet points",
        "use simple words",
        "make it shorter",
        "explain more simply"
    ]

    return any(
        phrase in text
        for phrase in feedback_phrases
    )


def is_market_analysis_request(message):
    text = message.lower()

    analysis_phrases = [
        "analyze bitcoin",
        "analyse bitcoin",
        "analyze btc",
        "bitcoin analysis",
        "btc analysis",
        "analyze the market",
        "bitcoin price",
        "latest bitcoin",
        "analyze bitcoin market"
    ]

    return any(
        phrase in text
        for phrase in analysis_phrases
    )



def analyze_bitcoin(user_message):
    # 1. Save the user's message
    short_memory.add_message("user", user_message)

    
    # Handle explicit feedback before fetching market data
    
    feedback_detected = detect_user_feedback(user_message)

    if feedback_detected:
        record_user_feedback(user_message)

        lower_message = user_message.lower()

        if (
            "future responses" in lower_message
            or "in future" in lower_message
            or "from now on" in lower_message
        ):
            long_memory.update(
                "explanation_style",
                "three short bullet points, simple language"
            )

        # If the message is only feedback, do not fetch market data.
        if not is_market_analysis_request(user_message):
            answer = (
                "Thanks for the feedback. "
                "I'll aim to use simpler words and shorter responses."
            )

            short_memory.add_message("assistant", answer)
            return answer

    # If the user also requested market analysis, continue below.



    # 2. Get Bitcoin market data
    market_data = get_btc_analysis()

    # 3. Read saved user preferences
    risk = long_memory.get("risk_tolerance", "unknown")
    horizon = long_memory.get("investment_horizon", "unknown")
    knowledge = long_memory.get("knowledge_level", "beginner")
    style = long_memory.get("explanation_style", "clear and simple")

    
    # Read recent episodic memories
    recent_episodes = episodic_memory.get_recent(limit=10)

    # Keep user feedback and ignore unrelated events
    feedback_episodes = [
        episode
        for episode in recent_episodes
        if episode.get("event") == "user_feedback"
    ]

    # Convert feedback records into readable text
    if feedback_episodes:
        feedback_context = "\n".join(
            f"- {episode['details']}"
            for episode in feedback_episodes
        )
    else:
        feedback_context = "No previous feedback available."


    # 4. Create the system instructions
    system_prompt = f"""
You are a careful Bitcoin analysis assistant.

Use the supplied market data as the source of truth.
Do not invent prices, indicators, or trends.
Do not claim a long-term trend from short-term indicators alone.
Explain uncertainty and never guarantee future prices.

User preferences:
- Risk tolerance: {risk}
- Investment horizon: {horizon}
- Knowledge level: {knowledge}
- Explanation style: {style}


Recent user feedback:
{feedback_context}

Use this feedback to improve your responses.
For example, if the user said previous explanations were too complicated,
use simpler words and shorter sentences.

Do not treat a single past comment as a permanent preference
if it conflicts with the user's current request or saved preferences.


Adapt your explanation to both the user's knowledge level
and preferred explanation style.

Follow the requested explanation style as closely as possible.
If the style is "simple English", use short sentences,
common words, and explain technical terms simply.
This is informational analysis, not guaranteed investment advice.

Preference management:
- When the user explicitly states or changes a preference,
  use the save_user_preference tool.
- Choose only the preference category that matches the user's request.
- Do not claim a preference was saved unless the tool confirms it.
- If the user's intent is unclear, ask for clarification.
- Never change a saved preference based only on a guess.
- Do not recommend specific buying, selling, or stop-loss actions
  based only on the supplied indicators.
- Explain what the indicators show, but separate observations
  from possible interpretations.
- Never describe the long-term trend using only the 7-day
  and 25-day moving averages.
- If a preference tool succeeds, acknowledge the saved preference
  briefly and then answer the user's request.
  


Feedback management:
- If the user explicitly criticizes a previous response or asks
  for an improvement to future responses, you MUST call
  record_feedback before replying.
- Do not merely acknowledge feedback without calling the tool.
- Do not call record_feedback for an ordinary Bitcoin question.
- After the tool confirms successful storage, briefly acknowledge it.
- Never claim feedback was saved unless the tool confirms success.


  
Analysis rules:
- Do not recommend specific buying, selling, or stop-loss actions
  based only on the supplied indicators.
- Explain what the indicators show and separate facts from interpretations.
- Do not describe the long-term trend using only SMA_7 and SMA_25.
- Never guarantee future Bitcoin prices.
- If a preference tool succeeds, briefly confirm the saved preference.
- Use previous user feedback to improve future explanations.
- RSI below 30 is commonly considered oversold.
- RSI above 70 is commonly considered overbought.
- RSI below 50 alone does not mean oversold.
- Treat these thresholds as common guidelines, not guarantees.

"""

    # 5. Build the conversation history
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    messages.extend(short_memory.get_messages())

    # 6. Add the current market data to the latest user message
    messages[-1]["content"] += (
        "\n\nLatest Bitcoin market data:\n"
        + str(market_data)
    )

    # 7. Ask the language model
    
    
    
    # 7. Ask the model and provide the available tool
    available_tools = (
        [preference_tool]
        if feedback_detected
        else [preference_tool, feedback_tool]
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=available_tools,
        tool_choice="auto",
        temperature=0.3
    )

    message = response.choices[0].message

    
    # 8. Execute requested tools
    max_tool_rounds = 3
    tool_round = 0

    while message.tool_calls and tool_round < max_tool_rounds:
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                tool_call.model_dump(exclude_none=True)
                for tool_call in message.tool_calls
            ]
        })

        for tool_call in message.tool_calls:
            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                tool_name = tool_call.function.name

                if tool_name == "save_user_preference":
                    result = save_user_preference(
                        arguments["key"],
                        arguments["value"]
                    )

                elif tool_name == "record_feedback":
                    result = record_user_feedback(
                        arguments["feedback"]
                    )

                else:
                    result = "Error: unknown tool."

            except (ValueError, KeyError, TypeError):
                result = "Error: invalid tool arguments."

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=available_tools,
            tool_choice="auto",
            temperature=0.3
        )

        message = response.choices[0].message
        tool_round += 1

    # 9. Get the final answer
    if message.tool_calls:
        answer = (
            "I couldn't finish processing the tool requests. "
            "Please try again."
        )
    else:
        answer = message.content or "No response was generated."

    # 10. Save the assistant's answer
    short_memory.add_message("assistant", answer)

    # 11. Record the interaction
    episodic_memory.add_episode(
        "bitcoin_analysis",
        f"User request: {user_message}"
    )

    return answer
