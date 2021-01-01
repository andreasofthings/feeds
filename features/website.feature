Feature: Websites Management

Scenario: List all Websites
  Given the user navigates to the website list
  When the user ain't logged in
  Then the user will see all websites in alphabetical order!
