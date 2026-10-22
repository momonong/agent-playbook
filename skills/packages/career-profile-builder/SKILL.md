---
name: career-profile-builder
description: Deepen an existing career profile or revise resume and LinkedIn experience descriptions using confirmed ownership, decisions, outcomes, and evidence. Use for career-material discovery and editing; tailor to a JD when provided. Reuse prior answers and accepted presentation choices.
---
# Career Profile Builder

Locally adapted from Vignesh Pai's `vignzpie/resume-agent-skills`, revision `d21f62ec07966a6f9b7963c5d1d8c736265d8393` (MIT license). Original entrypoint: [upstream-skill.md](references/upstream-skill.md); license: [LICENSE](LICENSE). The original is provenance, not the active workflow. This adaptation adds evidence-based editing for LinkedIn and resumes, removes mandatory full-profile interviews and career-level formatting assumptions, and uses the user's established files instead of forcing a new schema.

## Route by the requested output

- For discovery or a complete profile, start from existing material and identify actual gaps. Use [branching-questions.md](references/branching-questions.md), reading only relevant track sections. Treat it as an optional question bank, not a checklist or seniority policy.
- For LinkedIn or resume edits, first read [editorial-guidelines.md](references/editorial-guidelines.md). When facts are sufficient, edit immediately instead of restarting the interview.
- For JD tailoring, map stated requirements to confirmed experience. Change emphasis, selection, and wording without changing facts or official titles. Describe matches and gaps in words; do not invent ATS scores or hiring probabilities.
- Use [profile-template.md](references/profile-template.md) only if a full profile is requested and no established structure exists. It is optional. Drafts can stay in chat; save only as requested or clearly within the user's authorized artifact work.

## Discover useful evidence

Read the existing resume, supplied notes, and confirmed conversation facts before asking questions. Reuse answers; flag contradictions rather than silently choosing the more impressive claim.

For each relevant experience, distinguish:
- The original problem and who encountered it.
- The individual's actions, decisions, and implementation from team work.
- What changed and how that was observed or evaluated.
- Scope, constraints, alternatives, and tradeoffs when these explain the contribution.
- Unknowns, confidential details, and wording the user has explicitly ruled out.

Choose only the missing questions that could change the draft. Do not seek a confidential business domain or implementation detail when an abstract description suffices. Do not force a career label before the evidence is understood. Systems design, requirements work, and collaboration can support multiple roles without proving formal management experience.

## Preserve factual boundaries

Never invent metrics, roles, technology use, dates, deployment, or adoption. Preserve official employment titles unless the user verifies a correction. A plausible estimate needs a defensible basis and must remain identified as an estimate when used.

Distinguish implementation, evaluated cases, production deployment, active adoption, and business impact. A host system's existing user base is not usage of a new feature. Code and test records establish implementation and those tests, not user adoption. Keep simulation and evaluation conditions attached to relevant results.

When a number is unavailable, use the observed qualitative outcome. Do not replace the missing number with unsupported adjectives such as significant, scalable, or robust. Preserve the user's approved factual boundaries, while allowing sentence editing when requested.

## Edit and assess

Identify what the reader should remember about the experience. Use problem/action/result as a drafting aid, not a rigid sentence formula. Select the facts that establish that message; leave detailed interview notes out of the public copy.

Check each passage for:
1. Clear relevance to the intended reader or role family.
2. Specific individual contribution and meaningful technical detail.
3. Supported outcome with appropriate scope.
4. No repeated claim, inflated adjective, or filler.
5. Easy scanning in the destination's actual format.

Keep accepted formatting during a wording-only edit. For an authorized structural revision, explain the concrete reason for regrouping or reordering. Do not alternate between formats because of the latest isolated objection. Separate source-backed principles from local editorial choices, including bullet counts and heading styles.

Deliver one recommended version with a brief explanation of substantive changes. Supply alternatives only when they resolve a meaningful tradeoff or the user asks. Do not call a draft best practice, recruiter-approved, or final merely because it follows this skill. Skill validation checks structure; user review and actual outcomes remain distinct.

Installing or using this skill does not authorize publishing, contacting people, or putting private career notes in a public repository. Keep personal facts outside the reusable skill.
