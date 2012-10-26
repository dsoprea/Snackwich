
def get_window3(key, results, context):

    if 'test_val' in context:
        if context['test_val'] == 4:
            raise BreakSuccessionException()
        else:
            context['test_val'] += 1
    else:
        context['test_val'] = 1

    # We add a "_next" meta-attribute to tell it to go to a specific panel, 
    # next. We also add a timer_ms attribute to put a timer on the current 
    # panel, to automatically advance it.

    return { '_widget': 'list',
             '_next' : 'window99',
             'title': 'Title 3 (%d)' % (context['test_val']),
             'text': 'Text content',
             'items': [ ('Option 1', 'option1')
                      ],
             'default': 0,
             'scroll': 0,
             'height': 5,
             'timer_ms': 1000
           }

config = [{
    '_name': 'window1',
    '_widget': 'list',
    'title': 'Title 1',
    'text': 'Text content',
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
    'height': 5
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
    'width': 70
},
('window99', get_window3),
]

