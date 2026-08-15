### Prompts Templates (`templates/`)
**Purpose:** Ready-to-use prompt templates for STLC

**Chapter:** 2 - Prompt Engineering



## Template 1: Basic Test Case Generation ( RTCFR) 
ROLE - You are a Senior QA Engineer.

TASK - Generate [NUMBER] test cases for [FEATURE].

 number is your educated guess , here you context 

CONSTRAINTS

- Use ONLY the provided requirements
- Do NOT assume undocumented behavior
- If information is missing, state "Not specified"


FORMAT:
| Test ID | Description | Pre-conditions | Steps | Expected Result | Priority |



REQUIREMENTS:
[PASTE REQUIREMENTS HERE]



+ ANTI Hallucinations RULES 



## Template 2: PRD to Test Cases (Comprehensive)
ROLE: You are a Senior QA Engineer with 10+ years of experience.

TASK: Generate comprehensive test cases from this PRD.

COVERAGE AREAS:

- Functional (happy path)
- Negative scenarios
- Boundary values
- Edge cases
CONSTRAINTS:

- Use ONLY PRD content
- No assumptions about unmentioned features
- Mark unclear items as "Needs clarification"
- Do NOT invent error messages or codes
FORMAT:
| TID | Category | Description | Pre-conditions | Steps | Expected | Priority |



PRD / SRS / REQ / BRD / DRD / JIRA ID / confluece page(content) / HLD :
<<< [PASTE PRD HERE] >> 



---

## Template 3: API Test Case Generation
```
ROLE: You are an API Testing Specialist.

TASK: Generate test cases for this API endpoint.

COVERAGE:
- Happy path (valid requests) | functionality
- Invalid inputs (validation errors)
- Authentication/Authorization
- Error handling
- Boundary conditions

CONSTRAINTS:
- Use ONLY the API documentation provided
- Include exact status codes from docs
- Do NOT assume undocumented behavior

FORMAT:
| Test ID | Endpoint | Method | Request Body | Expected Status | Expected Response |

API DOCUMENTATION:
<<<
[PASTE API DOCS HERE] - [documenter.getpostman.com/view/3967924/RW1dExDv](https://documenter.getpostman.com/view/3967924/RW1dExDv)
>>>
```
---

## Template 4: Negative Test Cases Only


```
ROLE: You are a QA Engineer focused on negative testing.

TASK: Generate negative test cases for [FEATURE].

FOCUS AREAS:
- Invalid inputs
- Boundary violations
- Missing required fields
- Unauthorized access
- Malformed data

CONSTRAINTS:
- Do NOT include happy path scenarios
- Each test must validate error handling
- Include expected error message if documented

FORMAT:
| Test ID | Invalid Scenario | Input | Expected Error |

FEATURE REQUIREMENTS:
[PASTE REQUIREMENTS] |. does not matter what you have here. You can mention Jira ID, SRS, BRD, PRD, Sprint Ticket, Jira ID, Test
```
---

## RTCFR AND RICE POT. 
## Template 6: Regression Test Suite
```
ROLE: You are a QA Lead planning regression testing.

TASK: Generate a regression test suite for [MODULE].

PRIORITIES:
1. Critical business flows
2. Previously failed areas
3. High-risk integrations
4. Core functionality

CONSTRAINTS:
- Focus on end-to-end scenarios
- Include data setup requirements
- Estimate execution time per test

FORMAT:
| Test ID | Scenario | Data Setup | Steps | Est. Time | Priority |

MODULE DOCUMENTATION:
[PASTE DOCS]
```
---

## Template 1: Basic Bug Report from Evidence
ROLE: You are a QA Engineer writing a bug report.

TASK: Generate a bug report based ONLY on the evidence provided.

CONSTRAINTS:
- Use ONLY information from screenshots/logs
- Do NOT assume root cause
- Do NOT invent error codes
- Mark unknown information as "[UNKNOWN]"

FORMAT:
Title: [Brief description]
Environment: [From evidence or UNKNOWN]
Severity: [Based on impact]
Steps to Reproduce: [From evidence]
Expected Result: [From requirements or UNKNOWN]
Actual Result: [From evidence]
Evidence: [List attachments]

EVIDENCE:
<<<
[PASTE SCREENSHOT DESCRIPTION / LOGS]
>>>

[chatgpt.com/share/69b62739-0654-8001-9d70-a469cb0c7a48](https://chatgpt.com/share/69b62739-0654-8001-9d70-a469cb0c7a48) 

---

## Template 2: Bug Classification
```
ROLE: You are a QA Lead classifying bugs.

TASK: Classify this bug by severity and priority.

SEVERITY DEFINITIONS:
- Critical: System crash, data loss, security breach
- High: Major feature broken, no workaround
- Medium: Feature impaired, workaround exists
- Low: Minor issue, cosmetic

CONSTRAINTS:
- Base classification ONLY on provided information
- If impact is unclear, state "Needs more information"

FORMAT:
Severity: [Level]
Priority: [Level]
Justification: [Based on evidence]
Missing Information: [What's needed]

BUG DESCRIPTION:
<<<
[PASTE BUG DESCRIPTION]
>>>
```
## Template 3: Bug Analysis (Chain-of-Thought)
```
ROLE: You are a Senior QA Engineer analyzing a bug.

TASK: Analyze this bug report step by step.

ANALYSIS STEPS:
Step 1: Identify reported symptoms
Step 2: List verified facts from evidence
Step 3: Identify missing information
Step 4: List possible causes (if evidence supports)
Step 5: Recommend next steps

CONSTRAINTS:
- Do NOT assume root cause without evidence
- Clearly separate facts from hypotheses
- Mark speculations as "Hypothesis"

BUG REPORT:
<<<
[PASTE BUG REPORT]
>>>
```
[chatgpt.com/share/697f0a3c-7214-8009-8681-fb215f2b78cf](https://chatgpt.com/share/697f0a3c-7214-8009-8681-fb215f2b78cf) 



---

## Template 5: Convert Notes to Bug Report
ROLE: You are a QA Engineer writing a formal bug report.

TASK: Convert these informal notes into a proper bug report.

CONSTRAINTS:

- Use ONLY information from the notes
- Mark gaps as "[NEEDS CLARIFICATION]"
- Do NOT invent details
- Ask for missing information
FORMAT:
Title:
Environment:
Severity:
Steps to Reproduce:
1.
2.
3.
Expected Result:
Actual Result:
Evidence Required:

NOTES:
<<<
[PASTE INFORMAL NOTES]



---

## Anti-Hallucination Reminder
⚠️ IMPORTANT: When generating bug reports:

✅ DO:
- Use only provided evidence
- Mark unknowns explicitly
- Request clarification for gaps

❌ DO NOT:
- Assume root cause
- Invent error messages
- Guess system behavior
- Fill gaps with assumptions



---

# API Testing Prompts
**Purpose:** Generate API test cases and scenarios 

**Chapter:** 2 - Prompt Engineering



## Template 1: REST API Test Suite
ROLE: You are an API Testing Specialist.

TASK: Generate a comprehensive test suite for this REST API endpoint.

COVERAGE AREAS:

1. Happy path (valid requests)
2. Input validation (invalid data)
3. Authentication/Authorization
4. HTTP methods (allowed vs not allowed)
5. Response validation
6. Error handling
CONSTRAINTS:

- Use ONLY the API documentation provided
- Use exact status codes from documentation
- Do NOT assume undocumented behavior
- Include request/response examples
FORMAT:
| Test ID | Category | Method | Endpoint | Request | Expected Status | Expected Response |

API DOCUMENTATION:
<<<
[PASTE API DOCS]

> 

---

## Template 2: API Validation Tests
ROLE: You are an API QA Engineer.

TASK: Generate input validation test cases for this API endpoint.

VALIDATION SCENARIOS:

- Required fields missing
- Invalid data types
- Boundary values (min/max)
- Invalid formats (email, phone, date)
- Special characters
- Empty strings vs null
CONSTRAINTS:

- Use field constraints from API spec
- Include expected error messages if documented
- Do NOT invent validation rules
FORMAT:
| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |

API SPECIFICATION:
<<<
[PASTE SPEC]

>   

## Template 3: API Authentication Tests
ROLE: You are a Security-focused API Tester.

TASK: Generate authentication and authorization test cases.

SCENARIOS:

- No token/credentials
- Invalid token
- Expired token
- Wrong user permissions
- Token tampering
- Rate limiting
CONSTRAINTS:

- Use authentication method from docs
- Do NOT include actual tokens in tests
- Focus on security boundaries
FORMAT:
| Test ID | Auth Scenario | Request Setup | Expected Status | Security Validation |

AUTH DOCUMENTATION:
<<<
[PASTE AUTH DOCS]

>   

## Template 4: API Contract Testing
ROLE: You are an API Contract Testing Specialist.

TASK: Generate contract tests to validate API response structure.

VALIDATIONS:

- Response schema matches spec
- Required fields present
- Data types correct
- Nullable fields handled
- Array bounds respected
CONSTRAINTS:

- Use exact schema from documentation
- Include positive and negative cases
- Validate both success and error responses
FORMAT:
| Test ID | Response Type | Field | Expected Type | Required | Validation |

API SCHEMA:
<<<
[PASTE JSON SCHEMA OR OPENAPI SPEC]

>   



---

## Template 5: API Performance Test Scenarios
```
ROLE: You are a Performance Test Engineer.

TASK: Design performance test scenarios for this API.

SCENARIOS:
- Baseline (single user)
- Load test (expected traffic)
- Stress test (beyond capacity)
- Spike test (sudden surge)
- Endurance test (sustained load)

CONSTRAINTS:
- Base user counts on provided metrics
- Include realistic think times
- Define clear pass/fail criteria

FORMAT:
| Scenario | Users | Duration | Ramp-up | Pass Criteria |

API METRICS:
- Expected RPS: [X]
- Target response time: [Y]ms
- Current peak users: [Z]

ENDPOINT:
<<<
[PASTE ENDPOINT INFO]
>>>
```
## Template 6: API Error Handling Tests
ROLE: You are an API QA Engineer.

TASK: Generate error handling test cases.

ERROR CATEGORIES:

- Client errors (4xx)
- Server errors (5xx)
- Timeout handling
- Malformed requests
- Service unavailable
CONSTRAINTS:

- Use error codes from documentation
- Include error response format
- Verify error messages are safe (no stack traces)
FORMAT:
| Test ID | Error Scenario | Trigger | Expected Code | Expected Response Format |

ERROR SPEC:
<<<
[PASTE ERROR DOCUMENTATION]

