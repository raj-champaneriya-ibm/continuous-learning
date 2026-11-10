Feature: Every registered simulator adapter honors the run contract
  Scenario Outline: Run a dataset case with a scripted adapter
    Given adapter "<adapter>" has a scripted model
    When the adapter runs dataset case "c07"
    Then its run has the common draft schema and valid spans
    And its run retains the frozen version and pins

    Examples:
      | adapter           |
      | studio-langgraph  |
      | spec-langgraph    |
      | lab-c3            |
      | lab-version-b     |
      | offline           |
      | http-json         |
