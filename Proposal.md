# SEA710 – Project – Milestone 2

# Proposal

```
Total Mark: - 10 Marks (2.5% of the total course grade)
```
- Learn@Seneca Submission (Due: Monday October 27 at
    8:00am)

```
Submission file(s): - Project-Proposal.docx (this document with your answers)
```
Building on your initial ideas from Milestone 1, your group will now develop a clear,
structured, and feasible plan for your selected project topic. This milestone is your
opportunity to refine your concept, define your objectives, and plan the path forward.

Your proposal should clearly outline the problem you're addressing, the data and
resources you plan to use, and how your team will carry out the project through a realistic
timeline and clear task distribution.

## Part 1: Proposal Development

This section is designed to help your group define the scope and direction of your selected
project. Use it to clarify your goals, explore existing solutions, and plan your approach in
a structured and achievable way.

● Problem Definition, Objectives, and Final Deliverable
▪ Problem Description and Objective: What problem is your group aiming to solve?
What are your main goals for this project?
People with visual or reading impairments often need instant, context-aware answers
about their surroundings, such as identifying a product, reading expiration date, or
locating signs without depending on sighted assistance. Our goal is to create an AI-
powered assistant that allows a user to point a camera, ask a question (by voice or text),
and receive a spoken answer describing what is seen.

```
▪ Starting Point: What existing approaches, tools, or methods address this problem?
What are their limitations? Include references or examples where relevant.
```

Existing tools like Seeing AI and Be My Eyes demonstrate strong scene-understanding
capabilities, yet they are closed-source, cloud-dependent, and not easily adaptable to
research contexts. Academic Visual Question Answering (VQA) models (BLIP-2, LLaVA,
ViLT) perform well on benchmark images but often misinterpret cluttered, real-world
assistive scenes. These approaches rarely optimize for:
● Question-guided region selection
● OCR robustness under low-contrast or blurry text common in real environments.
Our project extends these methods with a new front-end that bridged object detection,
OCR, and question-driven focus, allowing the model to understand exactly what part of
the image matters for accessibility.

▪ Final Deliverable: What will your group produce as the final output (e.g. a working
app, a predictive model, a dashboard, etc.)?
A working prototype either desktop/web app that:

1. Captures live frames from a webcam or phone.
2. Accepts a typed or spoken natural-language question.
3. Processes the visual input through a question-guided VQA pipeline.
4. Outputs a spoken and on-screen answer.
The final deliverable will include a short demo video, the project report, and code.

● Data and Resource Considerations
▪ Identify the datasets you plan to use. Are they publicly available, or will you need
to collect or request access?
They are publicly available, and we also plan to collect some more on our own.
● VizWiz-VQA: real questions from blind users, used for testing and limited fine-
tuning.
● VQA v2: general-purpose VQA dataset for pre-training baselines.
● Custom Captured Set: our own images of household objects, receipts, and signages
for testing our question-guided pipeline.
▪ Note any constraints or requirements (e.g., hardware needs, storage, compute
resources, ethical considerations).
● Collected images might exclude identifiable faces or addresses.
● Computation limits might require lightweight models.

● Timeline and Plan
▪ Provide a week-by-week breakdown until the final deadline.


```
▪ Include key milestones, checkpoints, and deliverables (e.g. dataset finalized,
development stages, testing, writing, presentation preparation).
```
```
Week Milestones / Activities
```
```
Oct 27 – Nov 2 Finalize model choices and repository setup. Implement camera
capture and simple UI prototype. Test baseline Visual Question
Answering (VQA) model (BLIP-2 or LLaVA) on sample
questions.
```
```
Nov 3 – Nov 9 Develop and test OCR pipeline using Tesseract with basic
preprocessing (CLAHE, thresholding). Integrate object detection
module (YOLOv8 or SSD). Collect small internal dataset for
testing.
```
```
Nov 10 – Nov 16 Implement Question-Guided Region Proposer (QGRP) to
combine OCR and object detection results. Connect QGRP
output to VQA model for end-to-end evaluation.
```
```
Nov 17 – Nov 23 Improve model prompting and evaluate baseline vs QGRP
accuracy. Analyze latency and add safety filters for uncertain
responses.
```
```
Nov 24 – Nov 30 Refine accessibility UI (larger buttons, readable text). Integrate
optional speech output and finalize testing results. Prepare
demo and visuals for presentation.
```
```
Dec 1 – Dec 7 Conduct final evaluation and record results. Complete project
report, slides, and demo video for final presentation week.
```
● Task Breakdown
▪ Clearly outline the roles and responsibilities of each group member.
▪ Indicate who will be responsible for each component (e.g., data collection,
preprocessing, model training, documentation, writing, etc.).


```
Member Responsibilities
```
```
Abby Fernandez Integrate VQA model and develop user interface. Manage
speech output integration and prepare final demo and slides.
```
```
Mirac Ozcan Build OCR pipeline (Tesseract + preprocessing). Collect and test
dataset for text extraction accuracy.
```
```
Rajini
Paranagamage
```
```
Implement object detection and develop Question-Guided
Region Proposer (QGRP). Run model performance and latency
tests.
```
```
All Members Collaborate on research, documentation, final report writing,
and presentation.
```
● (Optional) Gantt Chart
▪ To support your submission, include a simple Gantt chart that outlines your
planned schedule across the weeks of the project. The chart should clearly show
your timeline, major tasks, milestones, and group responsibilities.
▪ A basic Gantt chart is sufficient, as long as it communicates the structure of your
plan. You are free to use any format to create and submit your Gantt chart (e.g.
Excel Excel Gantt chart templates | Microsoft Create, Google Sheets, screenshots
from online tools, etc.).

## Part 2: Deliverable for Milestone 2

Complete the following and submit this document by the deadline through
Learn@Seneca:

● Group number and names of all group members
● Topic, Problem Definition, Objectives, and Final Deliverable
● Data and Resource Considerations
● Timeline and Plan
● Task Breakdown
● (Optional) Gantt Chart


