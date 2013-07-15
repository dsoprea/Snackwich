from snackwich.buttons import BTN_OK, BTN_CANCEL
from snackwich.exceptions import QuitException, GotoPanelException

def get_window3(sw, key, context, screen):
    return { '_widget': 'list',
             'title': 'Title 3',
             'text': 'Text content 3',
             'items': [ ('Option 1', 'option1')
                      ],
             'default': 0,
             'scroll': 0,
             'height': 5,
             'timer_ms': 1000
           }

def window2_post_cb(sw, key, result, expression, screen):
    if result['button'] == BTN_CANCEL[1] or result['is_esc']:
        raise QuitException()

    fields = dict(zip(('prompt1', 'prompt2', 'prompt3'), 
                      result['values']))

    if fields['prompt1'].strip() == '':
        raise GotoPanelException('validation_error')

# Required in order to Snackwich to find the actual configuration.
config = [{
        '_name': 'window1',
        '_widget': 'list',
        'title': 'Title 1',
        'text': 'Text content 1',
        'items': [ ('Option 1', 'option1'),
                   ('Option 2', 'option2'),
                   ('Option 3', 'option3'),
                   ('Option 4', 'option4'),
                   ('Option 5', 'option5'),
                   ('Option 6', 'option6'),
                   ('Option 7', 'option7'),
                   ('Option 8', 'option8'),
                   ('Option 9', 'option9')
                 ],
        'default': 4,
        'scroll': 1,
        'height': 5,
        '_next': 'window2',
    },
    {
        '_name': 'window2',
        '_widget': 'entry',
        'title': 'Title 2',
        'text': 'Text content 2',
        'prompts': [ 'Prompt 1',
                     'Prompt 2',
                     'Prompt 3'
                   ],
        'width': 70,
        '_next': 'window3',
        '_post_cb': window2_post_cb,
    },
    ('window3', get_window3),
    { '_name': 'validation_error',
      '_widget': 'choice',
      '_next': 'window2',
      'title': 'Error',
      'text': "Please fill the 'Prompt 1' field.",
      'buttons': ['OK'],
    }]

