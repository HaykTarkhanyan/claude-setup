---
name: morning
description: Daily briefing — check calendar, email, telegram, create today's note
---

# Morning Routine

Today's date is available in the system context. Use it for all date calculations.

## Step 1: Create today's daily file

- Path: `tasks/daily/YYYY-MM-DD-Day.md` (e.g., `2026-03-30-Mon.md`)
- Use `tasks/daily/template.md` as the base, replacing `{{DATE}}` with today's date and `{{DAY}}` with the day name
- If the file already exists, only update the Briefing sections (Calendar, Email, Telegram) — leave Tasks, Learning, Done, Notes untouched

## Step 2: Check Google Calendar

- Fetch events from **2 days ago** through **5 days ahead**
- In the Calendar section, list events grouped by day
- **Bold today's events** and mark them prominently
- Note any conflicts or back-to-back meetings

## Step 3: Check Gmail

- Search emails from the **last 7 days**
- Summarize notable/unread emails in the Email section
- Group by importance: urgent, follow-up, FYI
- Keep it concise — subject + sender + one-line summary

## Step 4: Check Telegram

- List chats with recent activity
- Read messages from the **last 3 days** across active chats
- Summarize key conversations in the Telegram section
- Flag anything that needs a response

## Step 5: Weather & local alerts

- Determine which city the user is in (default: Munich; check calendar for travel clues)
- Web search for today's weather forecast for that city
- Web search for any local disruptions: public transport strikes, major road closures, or events worth knowing about
- If in Munich: check if any upcoming days (next 5 days) have store closures due to public holidays (e.g., Feiertage — not regular Sunday closures). If so, flag it prominently so Hayk can shop ahead.
- Add a short `### Weather & Alerts` section to the daily file after Telegram

## Step 6: Pull tasks into today

- Read the current week's file from `tasks/weekly/` (format: `WNN-DD Mon - DD Mon - YYYY.md`, e.g. `W13-29 Mar - 4 Apr - 2026.md`) and `tasks/reminders.md`
- Scan `tasks/topics/*.md` for anything due or relevant today
- Add relevant items to today's `## Tasks` section
- Check `tasks/inbox.md` — if anything is unsorted, mention it

## Step 7: Show summary to user

After updating the daily file, show a brief conversational summary:
- What's on today (calendar)
- Anything urgent from email or telegram
- Upcoming deadlines in the next few days

Keep the summary short — 10-15 lines max. The detail is in the daily file.
