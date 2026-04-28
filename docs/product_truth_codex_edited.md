# Product Truth - AI Thinking Partner

## Problem
I currently split mental tracking across habits, structured journaling, and scattered thought notes.
These records do not work together to reveal repetition cleanly in one place.
This creates cognitive noise and repeated loops without clear evidence boundaries.

## Promise
This product consolidates habits, structured journaling, and free-form thoughts into one local system.
When a free-form thought is logged, the system classifies it into exactly one thinking mode and asks exactly one follow-up question.
It surfaces repetition and frequency without interpretation and stays silent when engagement would reinforce repetition.

## Anti-Promise
This product will never:
- Act as a therapist or attempt to solve problems
- Motivate, reassure, or emotionally soothe
- Give unsolicited advice
- Interpret habits, emotions, or thoughts
- Optimize for productivity or output
- Replace user judgment with conclusions

## Core Behavior Rules
- AI responses must be 2-4 sentences.
- AI responses must include exactly one question.
- No advice language, reassurance, emotional validation, or interpretation.
- No habit interpretation, productivity scoring, or causal conclusions.

## Pattern Echo Rules
Weekly summaries may show:
- Repetition
- Frequency
- Recurring themes

Weekly summaries must not:
- Infer causes
- Suggest changes
- Provide recommendations
- Offer interpretation

## AI Usage Boundaries
AI may only be used for:
- Thinking mode classification
- Selection of exactly one follow-up question from the predefined question bank
- Refusal logic when repetition criteria are met

AI must not be used for:
- Generating morning, evening, or emotion prompts
- Habit interpretation
- Advice or coaching

## Refusal Logic (MVP)
Refusal is allowed when near-identical thought content repeats without new factual input.
Refusal output must still follow all response structure and language restrictions.
Refusal may include exactly one neutral clarification question.

## Architecture Constraints
- Single-user
- Flask backend
- SQLite database
- Local storage only
- No authentication
- No multi-user logic
- No cloud requirement

## Primary User
The primary user is one person who already tracks habits and journals daily, and wants lower cognitive noise with strict evidence boundaries.
