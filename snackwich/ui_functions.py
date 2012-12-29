"""A utility function."""

from snack import ButtonBar, TextboxReflowed, Listbox, GridFormHelp, Scale, \
                  Checkbox
import types

# Show the dialog, wait for input or timeout, pop, and redraw screen.
RT_EXECUTEANDPOP = 1

# Show the dialog, wait for input or timeout. The dialog must be popped off the 
# screen and redrawn manually.
RT_EXECUTEONLY   = 2

# Show the dialog. The dialog must be popped off the screen and redrawn 
# manually.
RT_DRAWONLY      = 3

def ProgressWindow(screen, title, text, progress, max_progress=100, width=40, 
                   help=None, timer_ms=None, show_cancel=False, 
                   run_type=RT_EXECUTEANDPOP):
    """
    Render a panel with a progress bar and a "Cancel" button.
    """

    if progress > max_progress:
        raise OverflowError("Progress (%d) has exceeded max (%d)." % 
                            (progress, max_progress))
    
    scale_proportion = .80
    scale_width = int(width * scale_proportion)
    scale = Scale(scale_width, max_progress)
    scale.set(progress)
    
    g = GridFormHelp(screen, title, help, 1, 3)

    t = TextboxReflowed(width, text)
    g.add(t, 0, 0)

    g.add(scale, 0, 1, padding = (0, 1, 0, 1))

    if show_cancel:
        bb = ButtonBar(screen, ['Cancel'])
        g.add(bb, 0, 2, growx = 1)

    if timer_ms:
        g.form.w.settimer(timer_ms)

    (button, is_esc) = ActivateWindow(g, run_type, \
                                      button_bar=bb if show_cancel else None)

    return {'button': button, 
            'is_esc': is_esc, 
            'progress': progress, 
            'grid': g,
           }

def MessageWindow(screen, title, text, width=40, help=None, timer_ms=None, 
                  run_type=RT_EXECUTEANDPOP):
    """
    Render a panel with a message and no buttons. This is intended to
    proceed to the next panel, where some action is taken before 
    returning -its- expression. Meanwhile, this panel is left displayed. 
    Obviously, this panel's timer shouldn't be large, if not zero.
    """
    
    g = GridFormHelp(screen, title, help, 1, 3)

    t = TextboxReflowed(width, text)
    g.add(t, 0, 0)

    if timer_ms:
        g.form.w.settimer(timer_ms)

    (button, is_esc) = ActivateWindow(g, run_type)

    return {'is_esc': is_esc, 
            'grid': g,
           }

def ActivateWindow(g, run_type, button_bar=None, x=None, y=None):
    global RT_EXECUTEANDPOP, RT_EXECUTEONLY, RT_DRAWONLY

    if run_type == RT_DRAWONLY:
        g.draw()
        
        button = None
        is_esc = False
        
    else:
        if run_type == RT_EXECUTEANDPOP:
            rc = g.runOnce(x, y) 
        
        elif run_type == RT_EXECUTEONLY:
            rc = g.run(x, y)

        button = button_bar.buttonPressed(rc) if button_bar else None
        is_esc = (rc == 'ESC')
        
    return (button, is_esc)

def ManualPop(screen, refresh=True):
    screen.popWindow(refresh)

def CheckboxListWindow(screen, title, text, items, buttons = ('Ok', 'Cancel'), 
                       width=40, scroll=0, default=None, help=None, 
                       timer_ms=None, secondary_message=None, 
                       secondary_message_width=None, 
                       run_type=RT_EXECUTEANDPOP,
                       default_check_state=False,
                       default_check_states=None):

    if not default_check_states:
        default_check_states = [default_check_state 
                                for i 
                                in xrange(len(items))]
    elif len(default_check_states) != len(items):
        raise Exception("Number (%d) of check states does not match number of "
                        "items (%d)." % (len(default_check_states), 
                                         len(items)))

    primary_message_height = 1
    button_height = 1
    checklist_margin = 0
    
    rows = primary_message_height + \
           button_height + \
           (2 if secondary_message else 0) + \
           len(items) + \
           checklist_margin
    
    bb = ButtonBar(screen, buttons)
    t = TextboxReflowed(width, text)

    g = GridFormHelp(screen, title, help, 1, rows)
    
    row = 0
    
    g.add(t, 0, row)
    row += 1

    if secondary_message:
        if not secondary_message_width:
            secondary_message_width = width
    
        t2 = TextboxReflowed(secondary_message_width, secondary_message)
        g.add(t2, 0, row, padding = (0, 1, 0, 0))
        row += 1

    checkboxes = []

    i = 0
    for item in items:
        if (type(item) == types.TupleType):
            (text, state) = item
        else:
            text = item
            state = default_check_state

        padding = [0, 0, 0, 0]
        if i == 0:
            padding[1] = 1

        if i == len(items) - 1:
            padding[3] = 1

        checkbox = Checkbox(text, int(state))
        checkboxes.append(checkbox)

        g.add(checkbox, 0, row, padding)
        row += 1
        i += 1

    g.add(bb, 0, row, growx = 1)
    row += 1

    if timer_ms:
        g.form.w.settimer(timer_ms)

    (button, is_esc) = ActivateWindow(g, run_type, bb)

    values = [checkbox.selected() for checkbox in checkboxes]

    return {'checkboxes': values,
            'button':     button, 
            'is_esc':     is_esc, 
            'grid':       g,
           }

