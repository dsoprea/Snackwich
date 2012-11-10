"""A utility function."""

from snack import ButtonBar, TextboxReflowed, Listbox, GridFormHelp, Scale

# Show the dialog, wait for input or timeout, pop, and redraw screen.
RT_EXECUTEANDPOP = 1

# Show the dialog, wait for input or timeout. The dialog must be popped off the 
# screen and redrawn manually.
RT_EXECUTEONLY   = 2

# Show the dialog. The dialog must be popped off the screen and redrawn 
# manually.
RT_DRAWONLY      = 3

def ProgressWindow(screen, title, text, progress, max_progress=100, width=40, 
                   help=None, timer_ms=None, show_cancel=False, run_type=RT_EXECUTEANDPOP):
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

