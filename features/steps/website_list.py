from behave import given, when, then

"""
 Scenario: List all Websites
  4    Given we navigate to the website list
  5          when we aren't logged in
  6          then we will see all websites in alphabetical order!
  ~
"""


@given('we navigate to the website list')
def step_impl(context):
        pass


@when(u'we aren\'t logged in')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we aren\'t logged in')


@then(u'we will see all websites in alphabetical order!')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we will see all websites in alphabetical order!')
