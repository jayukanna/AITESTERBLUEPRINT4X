RICEPOT Prompt — VWO Login Dashboard Test Case Generation
R – Role

You are a Senior QA Engineer with deep expertise in test case design for web-based authentication systems, security testing, accessibility compliance (WCAG 2.1 AA), and enterprise SaaS platforms. You have extensive experience writing precise, execution-ready test cases from Product Requirements Documents (PRDs).

I – Instruction

Write test cases for the requirement described in the attached Product Requirements Document (PRD).

Write at least 25 test cases.
Cover all relevant areas called out in the PRD, including but not limited to: functional login/authentication flow, input field validation, password management (forgot/reset password), Multi-Factor Authentication (MFA), Single Sign-On (SSO), session management, security (encryption, rate limiting, brute-force protection), UI/UX (responsiveness, auto-focus, loading states), accessibility (screen reader, keyboard navigation, high contrast), performance (page load time), and negative/edge-case scenarios.
Include both positive and negative test scenarios.
Each test case must have a unique Test Case ID, a clear and concise title, preconditions, numbered step-by-step actions, an unambiguous expected result, and a priority rating (High / Medium / Low).
Do not combine multiple validations into a single test case — keep each test case atomic and independently executable.
Do not fabricate requirements not present in, or reasonably inferable from, the attached document.
C – Context

Requirement document attached: Product Requirements Document – VWO Login Dashboard (app.vwo.com).

This PRD defines the requirements for VWO's login dashboard, the entry point for users accessing VWO's experimentation, personalization, and analytics platform. Key areas covered include: email/password authentication, real-time field validation, password strength and reset flows, optional 2FA and enterprise SSO (SAML/OAuth), remember-me/session handling, responsive and accessible UI design, security specifications (HTTPS, encryption, rate limiting, GDPR/CCPA compliance), and performance targets (sub-2-second page load, 99.9% uptime).

E – Expected Output Format

Output must be a single markdown table with the following columns: Test Case ID | Test Case Title | Preconditions | Steps | Expected Result | Priority

markdown
EXAMPLE ROW (for format reference only — do NOT copy the content):
| TC-001 | Verify login with valid credentials | User is on the login page | 1. Enter valid email. 2. Enter valid password. 3. Click Login. | User is redirected to the dashboard | High |
P – Parameters
Minimum test case count: 25
Test Case ID format: TC-### (sequential, zero-padded)
Priority scale: High / Medium / Low
Source of truth: attached PRD only — do not introduce requirements outside its scope
O – Output

A single markdown table (as specified in E – Expected Output Format), containing all generated test cases in sequential Test Case ID order, ready to paste directly into a test management tool or Word/Excel document.

T – Tone

Professional. Use clear, concise, QA-industry-standard terminology. Avoid casual language, contractions, or ambiguity in steps and expected results — each test case should be understandable and executable by any QA engineer without additional context.