
import logging

from snack import SnackScreen, ListboxChoiceWindow, ButtonChoiceWindow, \
                  EntryWindow

class Snackwich(object):
    config = None

    # Some shorthand aliases to make the config nicer. These must be FROM'd 
    # into the current scope, above.
    aliases = { 'list':     ListboxChoiceWindow,
                'choice':   ButtonChoiceWindow,
                'entry':    EntryWindow
              }

    def __init__(self, config_filepath):
        self.read_config(config_filepath)

    def read_config(self, config_filepath):
        """Read and parse the given config file."""
    
        logging.info("Reading config from [%s]." % (config_filepath))
    
        try:
            with file(config_filepath) as f:
                raw_data = f.read()
        except:
            logging.exception("Could not read menu file-path [%s]." % 
                              (config_filepath))
            raise

        local_scope = { }

        try:
            compiled = compile(raw_data, '<string>', 'exec')
            eval(compiled, { '__builtins__': __builtins__ }, local_scope)
        except:
            logging.exception("Could not evaluate menu config from file-path "
                              "[%s]." % (config_filepath))
            raise

        if 'config' not in local_scope:
            message = "Config must assign itself to a variable named 'config'."
            
            logging.error(message)
            raise Exception(message)

        config = local_scope['config']

        if not isinstance(config, list):
            message = "Config from file-path [%s] is expected to be a list," \
                      "not [%s]." % (config_filepath, \
                                     config.__class__.__name__)

            logging.error(message)
            raise TypeError(message)

        self.config = config

    def __process_stanza(self, screen, key, expression):
        """Process a single expression (form) from the config."""

        if 'widget' not in expression:
            message = "'widget' value is not in the expression for key " \
                      "[%s]." % (key)

            logging.error(message)
            raise Exception(message)
    
        widget = expression['widget']
        del expression['widget']

        # We provide a couple of aliases in order to be more intuitive. If 
        # used, invoke the actual class, now.
        if isinstance(widget, str):
            if widget not in self.aliases:
                message = "Widget with name [%s] is not a valid alias. " \
                          "Please provide a correct alias or use an actual " \
                          "class." % (widget)
            
                logging.error(message)
                raise Exception(message)
            
            widget = self.aliases[widget]
        
        # Create the widget.
        
        try:
            return widget(screen=screen, **expression)
        except:
            logging.exception("Could not manufacture widget [%s] under key "
                              "[%s]." % (widget.__class__.__name__, key))
            raise

    def execute(self):
        """Render each successive screen."""

        logging.info("Rendering forms.")

        screen = SnackScreen()
        key = None

        try:
            results = { }
            form_num = len(self.config)
            i = 0
            for expression in self.config:
                # Allow there to be a function call or lambda that must be 
                # called to render the actual expression. This call will 
                # receive the past results as well as the current key. This 
                # will allow the current form to feed from previous forms.
                if isinstance(expression, tuple):
                    if len(expression) != 2 or \
                       not isinstance(expression[0], str) or \
                       not callable(expression[1]):

                        message = "As a tuple, an expression must be " \
                                  "(<string>, <callable>)."

                        logging.error(message)
                        raise Exception(message)

                    (key, expression_call) = expression

                    try:
                        expression = expression_call(key, results)
                    except:
                        logging.exception("Callable expression for key [%s] " 
                                          "threw an exception." % (key))
                        raise

                else:
                    if 'name' not in expression:
                        message = "'name' key not found in expression " \
                                  "(%d)." % (i)

                        logging.error(message)
                        raise Exception(message)

                    key = expression['name']
                    del expression['name']
                
                if not isinstance(expression, dict):
                    message = "Effective expression for key [%s] is not a " \
                              "dictionary." % (key)
                    
                    logging.exception(message)
                    raise TypeError(message)

                logging.info("Processing form stanza (%d) of (%d) with key "
                             "[%s]." % (i, form_num, key))

                try:                
                    results[key] = self.__process_stanza(screen, key, 
                                                         expression)
                except:
                    logging.exception("There was an exception while processing"
                                      " the stanza for key [%s]." % (key))
                    raise

                i += 1
        except:
            logging.exception("There was an exception while processing "
                              "config stanza with key [%s]." % (key))
            raise
        finally:
            screen.finish()

        return results

