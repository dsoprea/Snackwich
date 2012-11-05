"""A utility function."""

from snack import ButtonBar, TextboxReflowed, Listbox, GridFormHelp, Scale

def ProgressWindow(screen, title, text, progress, max_progress=100, width=40, 
                   help=None, timer_ms=None):
    """
    Render a panel with a progress bar and a "Cancel" button.
    """
    
    scale_proportion = .80
    scale_width = int(width * scale_proportion)
    scale = Scale(scale_width, max_progress)
    scale.set(progress)
    
    bb = ButtonBar(screen, ['Cancel'])
    t = TextboxReflowed(width, text)

    g = GridFormHelp(screen, title, help, 1, 3)
    g.add(t, 0, 0)
    g.add(scale, 0, 1, padding = (0, 1, 0, 1))
    g.add(bb, 0, 2, growx = 1)

    if timer_ms:
        g.form.w.settimer(timer_ms)

    rc = g.runOnce()

    return {'button': bb.buttonPressed(rc), 'is_esc': (rc == 'ESC'), 
            'progress': progress
           }

def MessageWindow(screen, title, text, width=40, help=None, timer_ms=None):
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

    rc = g.runOnce()

    return {'is_esc': (rc == 'ESC')}

