# Output Formats

## Compact table (default)

| ID | Title | Req | Type | Pri | Preconditions | Test data | Steps | Expected result |
|----|-------|-----|------|-----|---------------|-----------|-------|-----------------|

Steps are numbered inline (`1. ... 2. ...`). Keep titles action + condition: "Reject voucher one minute after expiry".

## Detailed card (manual scripts, UAT)

```text
TC-07  Reject voucher one minute after expiry            P1  Boundary
Req:            AC4, BR2
Preconditions:  SPRING10 valid 2027-03-01 00:00 to 2027-03-31 23:59 store time;
                test clock set to 2027-04-01 00:00; cart subtotal $50.00
Steps:
  1. Open checkout
  2. Type SPRING10 in the voucher field
  3. Click Apply
Expected:
  - No discount line is added
  - Message under the field: "SPRING10 expired on 31/03/2027."
  - Order total stays $50.00
Postconditions: none
```

UAT scripts: write steps in business language, add an "Actual result" and "Pass/Fail" column, and a sign-off line.

## Gherkin (BDD automation)

Group by feature, one Scenario per case, Scenario Outline for data-driven boundaries. Tag with IDs and priority so runs can be filtered.

```gherkin
Feature: Apply a voucher code at checkout

  @TC-05 @TC-06 @P1 @AC3
  Scenario Outline: Minimum subtotal boundary for WELCOME5
    Given voucher "WELCOME5" gives $5.00 off with a $30.00 minimum
    And my cart subtotal is <subtotal>
    When I apply voucher "WELCOME5"
    Then <outcome>

    Examples:
      | subtotal | outcome                                                    |
      | $29.99   | I see the message "Spend $0.01 more to use WELCOME5."      |
      | $30.00   | the order total before shipping is $25.00                  |
```

## CSV for import

Write UTF-8 with a byte-order mark when writing a file (so Excel shows symbols like − and € correctly; an inline CSV in chat cannot carry one, so tell the user to save it as "UTF-8 with BOM"), a header row, quote every field, and put multi-line steps inside one quoted field with line breaks. Use the column set for the target tool; when unknown, use the generic set (it opens in Excel and Google Sheets and maps easily in any tool's import wizard).

**Generic / Excel** (`templates/test-cases.csv`):
`ID, Title, Requirement, Type, Priority, Preconditions, Test Data, Steps, Expected Result, Automation Candidate`

**TestRail** (CSV import, map in the wizard):
`Title, Section, Type, Priority, References, Preconditions, Steps, Expected Result`
— References holds the requirement or ticket IDs. TestRail has no default test-data field: put data in Preconditions (or a custom field if the project has one). Priority defaults: P1 → High or Critical, P2 → Medium, P3 → Low; Type defaults include Functional, Security, Regression, Acceptance, Performance, Usability, Other. Projects can rename both, so say which mapping you used.

**Mapping this skill's Type to tools that have fixed type lists:** Positive, Negative, Boundary, State → Functional; Permission → Security; Integration → Functional (or Compatibility); Non-functional → Performance or Usability; Regression → Regression.

**Xray for Jira** (Test Case Importer, manual tests):
`Test ID, Summary, Description, Priority, Labels, Action, Data, Expected Result`
— one row per step; rows with the same Test ID form one test; Summary and Priority only on the first row.

**Zephyr Scale** (CSV import):
`Name, Objective, Precondition, Priority, Labels, Coverage (Issues), Step, Test Data, Expected Result`
— one row per step; repeat Name on each step row or leave it empty, matching the import option chosen.

Tool import screens change between versions; tell the user to confirm the column mapping in the import wizard before running a large import.
