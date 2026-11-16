# SocraticCode usability evaluation plan

## Purpose and status

Use this plan to evaluate whether three participants can understand the exercise
flow, four-step hint progression, submission feedback, and independent Solo Check.
This is a plan and blank recording template only; no participants have been tested
and no results are claimed.

The study is formative, not a test of learning effectiveness. Use the app's
scripted-only mode so participant code is not sent to an external service:

```bash
SOCRATICCODE_SCRIPTED_ONLY=1 streamlit run app.py
```

## Participant introduction

> Thank you for taking part. We are evaluating this SocraticCode prototype, not
> you. Please work through the tasks and say what you expect the interface to do.
> There are no wrong answers. I may take notes about actions and comments, but I
> will not collect your name or unrelated personal information. You may skip any
> question or stop at any time. The app uses scripted hints in this session and
> does not send your code to OpenAI. With your permission, I would like to record
> anonymized notes about what was easy or confusing.

## Consent and privacy checklist

- Explain the purpose, duration, tasks, note-taking, and how findings may be used.
- Obtain voluntary consent before starting. Participation and any recording are
  optional; ask separately before taking screenshots, photos, or audio/video.
- Use participant IDs `P1`, `P2`, and `P3`; do not record names or identifying
  details in the template.
- Do not collect unrelated personal information. Avoid including participant
  names, faces, or private content in screenshots.
- Use `SOCRATICCODE_SCRIPTED_ONLY=1`; confirm the visible mode label before asking
  participants to request hints. Do not enter a real API key into the study setup.
- Explain that drafts and progress are session-local and can be cleared with
  **Restart learning session**.
- Let participants stop or withdraw without needing to give a reason. Do not
  retain identifiable notes or recordings after the agreed evaluation period.

## Tasks

Give one task at a time without demonstrating the interface first. Observe silently
unless the participant is blocked; record any help you provide.

1. **Find the first task:** Describe what the app asks you to do and how you would
   start. Submit the starter code once, without changing it.
2. **Use progressive guidance:** Request the next hint. Explain what you think it
   means, then request the next hint. Notice whether the hints become more specific
   and whether previous guidance remains available.
3. **Revise and resubmit:** Edit the code after requesting a hint. Check whether
   your edits remain. Use this correction if a concrete target is helpful:

   ```python
   def calculate_average(numbers):
       return sum(numbers) / len(numbers)
   ```

   Submit and describe the feedback you receive.
4. **Continue in order:** Complete Exercise 2 and explain what made it available.
5. **Try the independent challenge:** Open the Solo Check, explain what makes it
   independent, submit once, then revise and submit again. Notice whether any hint
   controls are offered.
6. **Review and restart:** Describe the information in the final summary. Restart
   the session and check what was reset.

## Observation questions

Ask these after the participant completes the relevant action; avoid coaching:

- What do you think you should do next?
- How did you know which exercise was available?
- What changed between the hints? Could you find an earlier hint again?
- What did the submission message tell you to do?
- Did your code remain after requesting a hint or changing exercises?
- How did you know the Solo Check was independent? Did you look for a hint?
- What did the final summary measure, and what do you think it does not measure?
- Was there any point where the interface behaved differently from your expectation?

## Post-task questions

Ask for a 1–5 rating (1 = strongly disagree, 5 = strongly agree), followed by an
optional explanation:

1. I understood the goal of each exercise.
2. I understood how to request the next hint.
3. I could tell that hints became progressively more specific.
4. I understood the code-submission feedback.
5. I knew why later exercises were locked or unlocked.
6. I understood that the Solo Check had no hints.
7. I could tell which features used scripted behavior in this session.
8. I could complete the tasks without unexpected loss of my code.

Then ask: What was most confusing? What would you change first? Was anything
unnecessarily difficult or helpful?

## Results template

Copy this section once for each participant. Leave fields blank if not observed;
do not infer a participant's intent or outcome.

### Participant [P1/P2/P3]

- Date (optional):
- Consent confirmed: [ ] yes [ ] no — if no, do not start
- Session completed or stopped:
- Observer assistance given:
- Scripted-only mode label confirmed: [ ] yes [ ] no

| Task | Completed without help? | Observed action / exact comment | Hesitation, error, or help needed |
|---|---|---|---|
| Find first task and submit starter | | | |
| Request progressive hints | | | |
| Edit code and submit correction | | | |
| Complete Exercise 2 | | | |
| Complete Solo Check without hints | | | |
| Review dashboard and restart | | | |

| Post-task statement | Rating (1–5) | Optional explanation |
|---|---:|---|
| Understood each exercise goal | | |
| Understood hint progression | | |
| Understood submission feedback | | |
| Understood progression/unlocking | | |
| Understood Solo Check restrictions | | |
| Recognized scripted mode | | |
| Code was retained as expected | | |

- Most confusing moment:
- Most helpful element:
- Suggested first change:
- Other notes (anonymized):

## Reporting the findings

After sessions, summarize the number of participants who completed each task,
recurring observed difficulties, and ratings with the participant count. Separate
observations from interpretation and recommendations. Report the small sample and
any observer assistance; do not claim statistical significance or improved learning.
