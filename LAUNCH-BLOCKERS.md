# Launch blockers — client data required

Placeholder text has been removed from the site. Where data is missing, the
section now renders an honest alternative rather than a bracketed placeholder.
Supplying the data below fills those sections automatically.

## 1. Trainers — `src/build_data.py` → `TRAINERS`

Currently renders: an invitation to meet the trainer at a free demo class.

```python
TRAINERS = [
  {"name": "...", "role": "...", "experience": "11 years",
   "background": "...", "specialisms": "BIM & Revit", "photo": "trainer-1"},
]
```
Needs: name, credentials, years, background, and **written photo consent**.

## 2. Success stories — `src/build_data.py` → `STORIES`

Currently renders: what we do to move a learner from trained to employed.

```python
STORIES = [
  {"name": "...", "before": "B.Tech Mechanical, fresher", "track": "Product Design",
   "skills": "SolidWorks · GD&T", "role": "Design Engineer",
   "employer": "...", "consent": True},
]
```
Needs: **signed, dated consent** per person. Salary figures require consent
naming that specific disclosure.

## 3. Legal review — BEFORE GO-LIVE

`privacy-policy/`, `terms-conditions/`, `disclaimer/` are drafted and no longer
say so on the page. They still require review by the client's legal advisor,
including DPDP Act compliance and the correct registered entity name.
Marked in `build_pages3.py` with `# LAUNCH BLOCKER`.

## 4. Still outstanding (not visible on the site)

- Verified CADD Centre network figures — homepage trust strip omits them
- NSDC association wording — mentioned on About, needs permitted phrasing
- Authorised certification list per programme
- Fee bands, or confirm counselling-only
- Batch schedule feed
- 3D printer make/model/materials
- Workstation count and batch sizes
- Employer names permitted for the Recruitment Panel
- First Job Pakka terms — eligibility and qualifying programmes
- Photography of the Sector 14 centre (shot list in Document 1, §6.6)
- Opening hours — reconcile 9:30 site vs 9:00 Google Business Profile

## 5. Images

All imagery is currently representative, labelled "Illustrative image" or
"Representative project output". Those captions stay until real photography
and consented student work replace them.
