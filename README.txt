Snackwich is an adaptation of the Snack console UI framework. Snack is, itself,
a port of Newt to Python. Newt is the console UI framework used in Redhat 
console applications. As there is no readily available console menu system 
available for Curses, this is the best option out there, and it works like a
dream.

The only requirement is that the Snack framework is installed. Under Ubuntu,
this is the "python-newt" package. It includes "snack.py", along with the
requisite dynamic library.

Example (located in example/):

    from snackwich import Snackwich

    panels = Snackwich('example.snack.py')

    from pprint import pprint
    pprint(panels.execute())

example.snack.py:

    [{
        'name': 'window1',
        'widget': 'list',
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
        'name': 'window2',
        'widget': 'entry',
        'title': 'Title 2',
        'text': 'Text content 2',
        'prompts': [ 'Prompt 1',
                     'Prompt 2',
                     'Prompt 3'
                   ],
        'width': 70
    }]

The result of the panels.execute() call, above, after I pressed ENTER all of 
the way through the first screen, and then entered three values on the second 
screen before pressing the "Ok" button:

    {'window1': (None, 'option3'),
     'window2': ('ok', ('Input value 1', 'Input value 2', 'Input value 3'))}
    
The second screen, as it appears to the user (this is in color):
                                                                                
     ┌────────────────────────────┤ Title 2 ├────────────────────────────┐      
     │                                                                   │      
     │ Text content 2                                                    │      
     │                                                                   │      
     │                   Prompt 1 Input value 1_______                   │      
     │                   Prompt 2 Input value 2_______                   │      
     │                   Prompt 3 Input value 3_______                   │      
     │                                                                   │      
     │             ┌────┐                        ┌────────┐              │      
     │             │ Ok │                        │ Cancel │              │      
     │             └────┘                        └────────┘              │      
     │                                                                   │      
     │                                                                   │      
     └───────────────────────────────────────────────────────────────────┘      
                                                                                
                                                                                
  <Tab>/<Alt-Tab> between elements   |  <Space> selects   |  <F12> next screen  

As this is just a wrapper around the basic Snack functionality for the purpose 
of interfacing with a configuration file, and most of the values in the form 
expressions are sent directly as arguments to Snack, you may see the full array 
of properties for each expression by looking in the main snack.py file (in the 
required package, mentioned above).

