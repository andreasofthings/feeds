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


@when('we implement a test')
def step_impl(context):
    assert True is not False


@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False
