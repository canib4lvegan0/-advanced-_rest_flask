# Created by robsonss at 20/07/22
Feature: Home service feature
  # Enter feature description here

  Scenario: Everything is Ok
    When get request to / is made
    Then should return status code 200 Ok
    Then the response should have body
    """
    {
      "message": "This is the canib4lvegan0 homepage"
    }
    """
