# SocraticCode storyboard scenarios

These are reproducible scenarios for capturing evidence from the implemented
prototype. Use scripted-only mode so screenshots show scripted guidance and no
student code is sent to OpenAI. Do not label scripted responses as AI-generated.
No screenshots or live AI responses are included or claimed by this document.

## Preparation

From the project directory:

```bash
source .venv/bin/activate
SOCRATICCODE_SCRIPTED_ONLY=1 streamlit run app.py
```

Open the local address printed by Streamlit. Confirm the page says **Scripted-only
mode** before requesting a hint. The setting is per process and does not erase
`.env` or Streamlit secrets. Use **Restart learning session** before each scenario.
Capture the app window only; do not include terminal output, credentials, or
personal information in screenshots.

## Scenario 1 — Requesting progressive guidance

1. Restart and remain on Exercise 1.
2. Capture the initial code, exercise objective, and scripted-only label.
3. Click **Request hint (0/4)**, then capture Level 1 and the unchanged code.
4. Click the hint button individually for Levels 2, 3, and 4. Capture the visible
   history after each request or one final image showing the labelled sequence.
5. Confirm the labels say **Scripted fallback hint** or **Scripted hint**; do not
   describe these messages as AI output.

Suggested evidence captions: “Initial guided exercise in scripted-only mode” and
“Four scripted hints requested one at a time.”

## Scenario 2 — Correcting an incorrect solution

1. Restart the session.
2. In Exercise 1, keep or enter:

   ```python
   def calculate_average(numbers):
       return sum(numbers) // len(numbers)
   ```

3. Click **Check my code** and capture the actual incorrect-answer feedback.
4. Replace it with:

   ```python
   def calculate_average(numbers):
       return sum(numbers) / len(numbers)
   ```

5. Click **Check my code** and capture the actual success state. Do not claim that
   the evaluator ran the function; it compares AST structure without execution.

Suggested evidence caption: “Incorrect integer division is rejected; the expected
average expression is accepted by the structural checker.”

## Scenario 3 — Completing the independent Solo Check

1. Restart the session.
2. Complete Exercise 1 with the correction shown above.
3. Complete Exercise 2 with:

   ```python
   def is_even(number):
       return number % 2 == 0
   ```

4. Open **Solo Check: Return the larger number**. Capture the independence notice
   and confirm there is no **Request hint** control.
5. Submit an attempted answer, then revise it to:

   ```python
   def larger_of_two(first, second):
       if first > second:
           return first
       return second
   ```

6. Submit and capture the resulting summary. The summary is a session usage
   dashboard, not evidence of long-term learning.

Suggested evidence caption: “The Solo Check has no hint control and records the
submission outcome after the two guided exercises.”

## Screenshot handling

Take screenshots only after the described UI state is visible. Use truthful,
descriptive filenames such as `storyboard-1-scripted-hints.png`; do not edit the
image to imply a different label or outcome. If a screenshot includes an API-mode
label, ensure the label matches the mode used. Keep participant screenshots
anonymous and obtain separate consent before capturing a participant's actions.
