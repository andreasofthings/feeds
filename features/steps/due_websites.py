from behave import given, when, then

@given(u'we start the crawling process')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we start the crawling process')


@when(u'the crawler starts')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the crawler starts')


@then(u'he will be passed only webpages that had recent changes.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then he will be passed only webpages that had recent changes.')
