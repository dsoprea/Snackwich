Snackwich is an adaptation of the Snack console UI framework. Snack is, itself,
a port of Newt to Python. Newt is the console UI framework used in Redhat 
console applications. As there is no readily available console menu system 
for Curses under Python, this is the best option out there, and it works like a
dream.

The only requirement is that the Snack framework is installed. Under Ubuntu,
this is the "python-newt" package. It includes "snack.py", along with the
requisite dynamic library.

See the "test.py" script in the example/ directory.

┌─────────────┤ Title 1 ├─────────────┐
│                                     │
│ Text content 1                      │
│                                     │
│             Option 1  ↑             │
│             Option 2  ▒             │
│             Option 3                │
│             Option 4  ▒             │
│             Option 5  ↓             │
│                                     │
│     ┌────┐          ┌────────┐      │
│     │ Ok │          │ Cancel │      │
│     └────┘          └────────┘      │
│                                     │
│                                     │
└─────────────────────────────────────┘

Snackwich allows you to express your panels declaratively (as a static list-of-
dictionaries), a list of tuples describing callbacks, or a combination of both.

The config also allows each panel to have a posthook callback to check which 
values/choices were made, which button was pressed, or whether ESC was used to 
escape the panel. See the example.

Although the configuration allows you to define the succession of which
panels lead to which, the posthook callback can raise certain exceptions to 
jump to different panels, redraw the current panel, quit, etc.. (see 
snackwich.exceptions).

The previous two features can be combined to implement validation: check the
values, navigate to an error panel, and navigate back (the error panel must 
have a '_next' describing the name of the original dialog).

The result of the example menu is the following (the names of the panels are
'window1', 'window2', and 'window3'):

{'validation_error': {'button': 'ok',
                      'grid': <snack.GridFormHelp instance at 0xb6f7222c>,
                      'is_esc': False},
 'window1': {'button': None,
             'grid': <snack.GridFormHelp instance at 0xb6f73b4c>,
             'is_esc': False,
             'selected': 'option5'},
 'window2': {'button': 'ok',
             'grid': <snack.GridFormHelp instance at 0xb6f7234c>,
             'is_esc': False,
             'values': ('test value', '', '')},
 'window3': {'button': None,
             'grid': <snack.GridFormHelp instance at 0xb6f7296c>,
             'is_esc': False,
             'selected': 'option1'}}

