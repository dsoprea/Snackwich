"""Adjusted versions of the original functions."""

import types

from snack import ButtonBar, TextboxReflowed, Listbox, GridFormHelp, Grid, \
                  Entry, Label

from snackwich.ui_functions import RT_EXECUTEANDPOP, RT_EXECUTEONLY, \
                                   RT_DRAWONLY, ActivateWindow


# Added auto-pop disable: Rather than immediately popping the dialog of the 
# stack of currently-displayed panels, we allow this to be done manually, 
# later.

def ListboxChoiceWindow(screen, title, text, items, buttons = ('Ok', 'Cancel'), 
                        width=40, scroll=None, height=-1, default=None, help=None, 
                        timer_ms=None, secondary_message=None, 
                        secondary_message_width=None, 
                        run_type=RT_EXECUTEANDPOP):
    
    # Dustin: Added timer_ms parameter. Added secondary_message arguments. 
    #         Added result boolean for whether ESC was pressed. Results are now
    #         dictionaries. Added auto_pop parameter.
    
    if height == -1: 
        height = len(items)
    
    if scroll == None:
        scroll = len(items) > height

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
        elif (default == text):
            default = key

        l.append(text, key)
        count = count + 1

    if (default != None):
        l.setCurrent (default)

    g = GridFormHelp(screen, title, help, 1, 3 + (1 if secondary_message else 
                                                  0))
    
    row = 0
    
    g.add(t, 0, row)
    row += 1

    if secondary_message:
        if not secondary_message_width:
            secondary_message_width = width
    
        t2 = TextboxReflowed(secondary_message_width, secondary_message)
        g.add(t2, 0, row, padding = (0, 0, 0, 1))
        row += 1

    g.add(l, 0, row, padding = (0, 1, 0, 1))
    row += 1
    
    g.add(bb, 0, row, growx = 1)
    row += 1

    if timer_ms:
        g.form.w.settimer(timer_ms)

    (button, is_esc) = ActivateWindow(g, run_type, bb)

    return {'button': button, 
            'is_esc': is_esc, 
            'grid': g,

            # A hack. There's no count method.
            'selected': l.current() if l.key2item else None,  
           }

def ButtonChoiceWindow(screen, title, text, buttons=['Ok', 'Cancel'], width=40, 
                       x=None, y=None, help=None, timer_ms=None, 
                       secondary_message=None, secondary_message_width=None, 
                       run_type=RT_EXECUTEANDPOP):

    # Dustin: Added timer_ms parameter. Added secondary_message arguments. 
    #         Added result boolean for whether ESC was pressed. Results are now
    #         dictionaries. Added auto_pop parameter.

    bb = ButtonBar(screen, buttons)
    t = TextboxReflowed(width, text, maxHeight = screen.height - 12)

    g = GridFormHelp(screen, title, help, 1, 2 + (1 if secondary_message else 
                                                  0))

    row = 0

    g.add(t, 0, row, padding = (0, 0, 0, 1))
    row += 1

    if secondary_message:
        if not secondary_message_width:
            secondary_message_width = width
    
        t2 = TextboxReflowed(secondary_message_width, secondary_message)
        g.add(t2, 0, row, padding = (0, 0, 0, 1))
        row += 1

    g.add(bb, 0, row, growx = 1)
    row += 1

    if timer_ms:
        g.form.w.settimer(timer_ms)

    (button, is_esc) = ActivateWindow(g, run_type, bb, x, y)

    return {'button': button, 
            'is_esc': is_esc, 
            'grid': g,
           }

def EntryWindow(screen, title, text, prompts, allowCancel=1, width=40,
                entryWidth=20, buttons=[ 'Ok', 'Cancel' ], help=None, 
                timer_ms=None, anchorLeft=0, anchorRight=1, 
                secondary_message=None, secondary_message_width=None, 
                run_type=RT_EXECUTEANDPOP):

    # Dustin: Added timer_ms parameter. Added secondary_message arguments. 
    #         Added result boolean for whether ESC was pressed. Added 
    #         anchorLeft and anchorRight as arguments to this function. Added 
    #         secondary_message (test below primary text). Results are now
    #         dictionaries. Added auto_pop parameter.

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

        sg.setField(Label(n), 0, count, padding=(0, 0, 1, 0), 
                    anchorLeft=anchorLeft, anchorRight=anchorRight)
        sg.setField(e, 1, count, anchorLeft = 1)
        count = count + 1
        entryList.append(e)

    g = GridFormHelp(screen, title, help, 1, 3 + (1 if secondary_message else 
                                                  0))
    
    row = 0

    g.add(t, 0, row, padding = (0, 0, 0, 1))
    row += 1

    if secondary_message:
        if not secondary_message_width:
            secondary_message_width = width
    
        t2 = TextboxReflowed(secondary_message_width, secondary_message)
        g.add(t2, 0, row, padding = (0, 0, 0, 1))
        row += 1

    g.add(sg, 0, row, padding = (0, 0, 0, 1))
    row += 1
    
    g.add(bb, 0, row, growx = 1)
    row += 1

    if timer_ms:
        g.form.w.settimer(timer_ms)

    (button, is_esc) = ActivateWindow(g, run_type, bb)

    entryValues = []
    count = 0
    for n in prompts:
        entryValues.append(entryList[count].value())
        count = count + 1

    return {'button': button, 
            'is_esc': is_esc, 
            'values': tuple(entryValues), 
            'grid':   g,
           }

