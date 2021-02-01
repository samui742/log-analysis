from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from art import *
#pint program name
tprint('<<<Tar A. Interactive>>>')

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'checkbox',
        'message': 'Select variables for analysis',
        'name': 'toppings',
        'choices': [
            Separator('= Pick switch for analysis ='),
            {
                'name': 'All Switches',
                'checked': True
            },
            {
                'name': 'Switch1'
            },
            {
                'name': 'Switch2'
            },
            {
                'name': 'Switch3'
            },
            {
                'name': 'Switch4'
            },
            {
                'name': 'switch5'
            },
            Separator('= Errors to look for ='),
            {
                'name': 'FAILED VALIDATION!!',
                'checked': True
            },
            {
                'name': 'FAILED',
                'checked': True
            },
            {
                'name': 'FAIL**',
                'checked': True
            },
            {
                'name': 'err-disable',
                'checked': True
            },
            {
                'name': 'Write your own'
            },
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)
pprint(answers)
 