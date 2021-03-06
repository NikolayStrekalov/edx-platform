#pylint: disable=C0111
#pylint: disable=W0621

#EVERY PROBLEM TYPE MUST HAVE THE FOLLOWING:
# -Section in Dictionary containing:
#   -factory
#   -kwargs
#   -(optional metadata)
#   -Correct, Incorrect and Unanswered CSS selectors
# -A way to answer the problem correctly and incorrectly
# -A way to check the problem was answered correctly, incorrectly and blank

from lettuce import world
import random
import textwrap
from common import section_location
from capa.tests.response_xml_factory import OptionResponseXMLFactory, \
    ChoiceResponseXMLFactory, MultipleChoiceResponseXMLFactory, \
    StringResponseXMLFactory, NumericalResponseXMLFactory, \
    FormulaResponseXMLFactory, CustomResponseXMLFactory, \
    CodeResponseXMLFactory, ChoiceTextResponseXMLFactory


# Factories from capa.tests.response_xml_factory that we will use
# to generate the problem XML, with the keyword args used to configure
# the output.
PROBLEM_DICT = {
    'drop down': {
        'factory': OptionResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The correct answer is Option 2',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correct_option': 'Option 2'},
        'correct': ['span.correct'],
        'incorrect': ['span.incorrect'],
        'unanswered': ['span.unanswered']},

    'multiple choice': {
        'factory': MultipleChoiceResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The correct answer is Choice 3',
            'choices': [False, False, True, False],
            'choice_names': ['choice_0', 'choice_1', 'choice_2', 'choice_3']},
        'correct': ['label.choicegroup_correct', 'span.correct'],
        'incorrect': ['label.choicegroup_incorrect', 'span.incorrect'],
        'unanswered': ['span.unanswered']},

    'checkbox': {
        'factory': ChoiceResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The correct answer is Choices 1 and 3',
            'choice_type': 'checkbox',
            'choices': [True, False, True, False, False],
            'choice_names': ['Choice 1', 'Choice 2', 'Choice 3', 'Choice 4']},
        'correct': ['span.correct'],
        'incorrect': ['span.incorrect'],
        'unanswered': ['span.unanswered']},

    'radio': {
        'factory': ChoiceResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The correct answer is Choice 3',
            'choice_type': 'radio',
            'choices': [False, False, True, False],
            'choice_names': ['Choice 1', 'Choice 2', 'Choice 3', 'Choice 4']},
        'correct': ['label.choicegroup_correct', 'span.correct'],
        'incorrect': ['label.choicegroup_incorrect', 'span.incorrect'],
        'unanswered': ['span.unanswered']},

    'string': {
        'factory': StringResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The answer is "correct string"',
            'case_sensitive': False,
            'answer': 'correct string'},
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered']},

    'numerical': {
        'factory': NumericalResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The answer is pi + 1',
            'answer': '4.14159',
            'tolerance': '0.00001',
            'math_display': True},
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered']},

    'formula': {
        'factory': FormulaResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The solution is [mathjax]x^2+2x+y[/mathjax]',
            'sample_dict': {'x': (-100, 100), 'y': (-100, 100)},
            'num_samples': 10,
            'tolerance': 0.00001,
            'math_display': True,
            'answer': 'x^2+2*x+y'},
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered']},

    'script': {
        'factory': CustomResponseXMLFactory(),
        'kwargs': {
            'question_text': 'Enter two integers that sum to 10.',
            'cfn': 'test_add_to_ten',
            'expect': '10',
            'num_inputs': 2,
            'script': textwrap.dedent("""
                def test_add_to_ten(expect,ans):
                    try:
                        a1=int(ans[0])
                        a2=int(ans[1])
                    except ValueError:
                        a1=0
                        a2=0
                    return (a1+a2)==int(expect)
            """)},
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered']},

    'code': {
        'factory': CodeResponseXMLFactory(),
        'kwargs': {
            'question_text': 'Submit code to an external grader',
            'initial_display': 'print "Hello world!"',
            'grader_payload': '{"grader": "ps1/Spring2013/test_grader.py"}', },
        'correct': ['span.correct'],
        'incorrect': ['span.incorrect'],
        'unanswered': ['span.unanswered']},

    'radio_text': {
        'factory': ChoiceTextResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The correct answer is Choice 0 and input 8',
            'type': 'radiotextgroup',
            'choices': [("true", {"answer": "8", "tolerance": "1"}),
                        ("false", {"answer": "8", "tolerance": "1"})
                        ]
        },
        'correct': ['section.choicetextgroup_correct'],
        'incorrect': ['span.incorrect', 'section.choicetextgroup_incorrect'],
        'unanswered': ['span.unanswered']},

    'checkbox_text': {
        'factory': ChoiceTextResponseXMLFactory(),
        'kwargs': {
            'question_text': 'The correct answer is Choice 0 and input 8',
            'type': 'checkboxtextgroup',
            'choices': [("true", {"answer": "8", "tolerance": "1"}),
                        ("false", {"answer": "8", "tolerance": "1"})
                        ]
        },
        'correct': ['span.correct'],
        'incorrect': ['span.incorrect'],
        'unanswered': ['span.unanswered']}
}


def answer_problem(problem_type, correctness):
    if problem_type == "drop down":
        select_name = "input_i4x-edx-model_course-problem-drop_down_2_1"
        option_text = 'Option 2' if correctness == 'correct' else 'Option 3'
        world.browser.select(select_name, option_text)

    elif problem_type == "multiple choice":
        if correctness == 'correct':
            world.css_check(inputfield('multiple choice', choice='choice_2'))
        else:
            world.css_check(inputfield('multiple choice', choice='choice_1'))

    elif problem_type == "checkbox":
        if correctness == 'correct':
            world.css_check(inputfield('checkbox', choice='choice_0'))
            world.css_check(inputfield('checkbox', choice='choice_2'))
        else:
            world.css_check(inputfield('checkbox', choice='choice_3'))

    elif problem_type == 'radio':
        if correctness == 'correct':
            world.css_check(inputfield('radio', choice='choice_2'))
        else:
            world.css_check(inputfield('radio', choice='choice_1'))

    elif problem_type == 'string':
        textvalue = 'correct string' if correctness == 'correct' else 'incorrect'
        world.css_fill(inputfield('string'), textvalue)

    elif problem_type == 'numerical':
        textvalue = "pi + 1" if correctness == 'correct' else str(random.randint(-2, 2))
        world.css_fill(inputfield('numerical'), textvalue)

    elif problem_type == 'formula':
        textvalue = "x^2+2*x+y" if correctness == 'correct' else 'x^2'
        world.css_fill(inputfield('formula'), textvalue)

    elif problem_type == 'script':
        # Correct answer is any two integers that sum to 10
        first_addend = random.randint(-100, 100)
        second_addend = 10 - first_addend

        # If we want an incorrect answer, then change
        # the second addend so they no longer sum to 10
        if correctness == 'incorrect':
            second_addend += random.randint(1, 10)

        world.css_fill(inputfield('script', input_num=1), str(first_addend))
        world.css_fill(inputfield('script', input_num=2), str(second_addend))

    elif problem_type == 'code':
        # The fake xqueue server is configured to respond
        # correct / incorrect no matter what we submit.
        # Furthermore, since the inline code response uses
        # JavaScript to make the code display nicely, it's difficult
        # to programatically input text
        # (there's not <textarea> we can just fill text into)
        # For this reason, we submit the initial code in the response
        # (configured in the problem XML above)
        pass

    elif problem_type == 'radio_text' or problem_type == 'checkbox_text':

        input_value = "8" if correctness == 'correct' else "5"
        choice = "choiceinput_0bc" if correctness == 'correct' else "choiceinput_1bc"
        world.css_fill(
            inputfield(
                problem_type,
                choice="choiceinput_0_numtolerance_input_0"
            ),
            input_value
        )
        world.css_check(inputfield(problem_type, choice=choice))


def problem_has_answer(problem_type, answer_class):
    if problem_type == "drop down":
        if answer_class == 'blank':
            assert world.browser.is_element_not_present_by_css('option[selected="true"]')
        else:
            actual = world.browser.find_by_css('option[selected="true"]').value
            expected = 'Option 2' if answer_class == 'correct' else 'Option 3'
            assert actual == expected

    elif problem_type == "multiple choice":
        if answer_class == 'correct':
            assert_checked('multiple choice', ['choice_2'])
        elif answer_class == 'incorrect':
            assert_checked('multiple choice', ['choice_1'])
        else:
            assert_checked('multiple choice', [])

    elif problem_type == "checkbox":
        if answer_class == 'correct':
            assert_checked('checkbox', ['choice_0', 'choice_2'])
        elif answer_class == 'incorrect':
            assert_checked('checkbox', ['choice_3'])
        else:
            assert_checked('checkbox', [])

    elif problem_type == "radio":
        if answer_class == 'correct':
            assert_checked('radio', ['choice_2'])
        elif answer_class == 'incorrect':
            assert_checked('radio', ['choice_1'])
        else:
            assert_checked('radio', [])

    elif problem_type == 'string':
        if answer_class == 'blank':
            expected = ''
        else:
            expected = 'correct string' if answer_class == 'correct' else 'incorrect'
        assert_textfield('string', expected)

    elif problem_type == 'formula':
        if answer_class == 'blank':
            expected = ''
        else:
            expected = "x^2+2*x+y" if answer_class == 'correct' else 'x^2'
        assert_textfield('formula', expected)

    elif problem_type in ("radio_text", "checkbox_text"):
        if answer_class == 'blank':
            expected = ('', '')
            assert_choicetext_values(problem_type, (), expected)
        elif answer_class == 'incorrect':
            expected = ('5', '')
            assert_choicetext_values(problem_type, ["choiceinput_1bc"], expected)
        else:
            expected = ('8', '')
            assert_choicetext_values(problem_type, ["choiceinput_0bc"], expected)

    else:
        # The other response types use random data,
        # which would be difficult to check
        # We trade input value coverage in the other tests for
        # input type coverage in this test.
        pass


##############################
#       HELPER METHODS
##############################

def add_problem_to_course(course, problem_type, extraMeta=None):
    '''
    Add a problem to the course we have created using factories.
    '''

    assert(problem_type in PROBLEM_DICT)

    # Generate the problem XML using capa.tests.response_xml_factory
    factory_dict = PROBLEM_DICT[problem_type]
    problem_xml = factory_dict['factory'].build_xml(**factory_dict['kwargs'])
    metadata = {'rerandomize': 'always'} if not 'metadata' in factory_dict else factory_dict['metadata']
    if extraMeta:
        metadata = dict(metadata, **extraMeta)

    # Create a problem item using our generated XML
    # We set rerandomize=always in the metadata so that the "Reset" button
    # will appear.
    category_name = "problem"
    return world.ItemFactory.create(parent_location=section_location(course),
                            category=category_name,
                            display_name=str(problem_type),
                            data=problem_xml,
                            metadata=metadata)


def inputfield(problem_type, choice=None, input_num=1):
    """ Return the css selector for `problem_type`.
    For example, if problem_type is 'string', return
    the text field for the string problem in the test course.

    `choice` is the name of the checkbox input in a group
    of checkboxes. """

    sel = ("input#input_i4x-edx-model_course-problem-%s_2_%s" %
           (problem_type.replace(" ", "_"), str(input_num)))

   # this is necessary due to naming requirement for this problem type
    if problem_type in ("radio_text", "checkbox_text"):
        sel = "input#i4x-edx-model_course-problem-{0}_2_{1}".format(
            problem_type.replace(" ", "_"), str(input_num)
        )

    if choice is not None:
        base = "_choice_" if problem_type == "multiple choice" else "_"
        sel = sel + base + str(choice)

    # If the input element doesn't exist, fail immediately
    assert world.is_css_present(sel)

    # Retrieve the input element
    return sel


def assert_checked(problem_type, choices):
    '''
    Assert that choice names given in *choices* are the only
    ones checked.

    Works for both radio and checkbox problems
    '''

    all_choices = ['choice_0', 'choice_1', 'choice_2', 'choice_3']
    for this_choice in all_choices:
        def check_problem():
            element = world.css_find(inputfield(problem_type, choice=this_choice))
            if this_choice in choices:
                assert element.checked
            else:
                assert not element.checked
        world.retry_on_exception(check_problem)


def assert_textfield(problem_type, expected_text, input_num=1):
    element_value = world.css_value(inputfield(problem_type, input_num=input_num))
    assert element_value == expected_text


def assert_choicetext_values(problem_type, choices, expected_values):
    """
    Asserts that only the given choices are checked, and given
    text fields have a desired value
    """
    # Names of the radio buttons or checkboxes
    all_choices = ['choiceinput_0bc', 'choiceinput_1bc']
    # Names of the numtolerance_inputs
    all_inputs = [
        "choiceinput_0_numtolerance_input_0",
        "choiceinput_1_numtolerance_input_0"
    ]
    for this_choice in all_choices:
        element = world.css_find(inputfield(problem_type, choice=this_choice))

        if this_choice in choices:
            assert element.checked
        else:
            assert not element.checked

    for (name, expected) in zip(all_inputs, expected_values):
        element = world.css_find(inputfield(problem_type, name))
        # Remove any trailing spaces that may have been added
        assert element.value.strip() == expected
