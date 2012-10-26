"""Adjusted versions of the original functions."""

import types

from snack import ButtonBar, TextboxReflowed, Listbox, GridFormHelp, Grid, \
                  Entry, Label

def ListboxChoiceWindow(screen, title, text, items, 
            buttons = ('Ok', 'Cancel'), 
            width = 40, scroll = 0, height = -1, default = None,
            help = None, timer_ms = 0):
    """
    - ListboxChoiceWindow(screen, title, text, items, 
            buttons = ('Ok', 'Cancel'), 
            width = 40, scroll = 0, height = -1, default = None,
            help = None):
    """
    
    # Dustin: Added timer_ms parameter.
    
    if (height == -1): height = len(items)

    bb = ButtonBar(screen, buttons)
    t = TextboxReflowed(width, text)
    l = Listbox(height, scroll = scroll, returnExit = 1)
    count = 0
    for item in items:
        if (type(item) == types.TupleType):
            (text, key) = item
        else:
            text = item
            key = count

        if (default == count):
            default = key
        elif (default == item):
            default = key

        l.append(text, key)
        count = count + 1

    if (default != None):
        l.setCurrent (default)

    g = GridFormHelp(screen, title, help, 1, 3)
    g.add(t, 0, 0)
    g.add(l, 0, 1, padding = (0, 1, 0, 1))
    g.add(bb, 0, 2, growx = 1)

    if timer_ms:
        g.form.w.settimer(timer_ms)

    rc = g.runOnce()

    return (bb.buttonPressed(rc), l.current())

def ButtonChoiceWindow(screen, title, text, 
               buttons = [ 'Ok', 'Cancel' ], 
               width = 40, x = None, y = None, help = None, timer_ms = 0):
    """
     - ButtonChoiceWindow(screen, title, text, 
               buttons = [ 'Ok', 'Cancel' ], 
               width = 40, x = None, y = None, help = None):
    """

    # Dustin: Added timer_ms parameter.

    bb = ButtonBar(screen, buttons)
    t = TextboxReflowed(width, text, maxHeight = screen.height - 12)

    g = GridFormHelp(screen, title, help, 1, 2)
    g.add(t, 0, 0, padding = (0, 0, 0, 1))
    g.add(bb, 0, 1, growx = 1)

    if timer_ms:
        g.form.w.settimer(timer_ms)

    return bb.buttonPressed(g.runOnce(x, y))

def EntryWindow(screen, title, text, prompts, allowCancel = 1, width = 40,
        entryWidth = 20, buttons = [ 'Ok', 'Cancel' ], help = None, 
        timer_ms = 0):
    """
    EntryWindow(screen, title, text, prompts, allowCancel = 1, width = 40,
        entryWidth = 20, buttons = [ 'Ok', 'Cancel' ], help = None):
    """

    # Dustin: Added timer_ms parameter.

    bb = ButtonBar(screen, buttons);
    t = TextboxReflowed(width, text)

    count = 0
    for n in prompts:
        count = count + 1

    sg = Grid(2, count)

    count = 0
    entryList = []
    for n in prompts:
        if (type(n) == types.TupleType):
            (n, e) = n
            if (type(e) in types.StringTypes):
                e = Entry(entryWidth, e)
        else:
            e = Entry(entryWidth)

        sg.setField(Label(n), 0, count, padding = (0, 0, 1, 0), anchorLeft = 1)
        sg.setField(e, 1, count, anchorLeft = 1)
        count = count + 1
        entryList.append(e)

    g = GridFormHelp(screen, title, help, 1, 3)

    g.add(t, 0, 0, padding = (0, 0, 0, 1))
    g.add(sg, 0, 1, padding = (0, 0, 0, 1))
    g.add(bb, 0, 2, growx = 1)

    if timer_ms:
        g.form.w.settimer(timer_ms)

    result = g.runOnce()

    entryValues = []
    count = 0
    for n in prompts:
        entryValues.append(entryList[count].value())
        count = count + 1

    return (bb.buttonPressed(result), tuple(entryValues))


