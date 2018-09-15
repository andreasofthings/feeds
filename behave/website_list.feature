Feature: Listing all Websites for an anonymous user

Scenario: List all Websites
   Given we navigate to the website list
         when we aren't logged in
         then we will see all websites in alphabetical order!
