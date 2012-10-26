
import logging
import copy

from snack import SnackScreen

from snackwich.patch import ListboxChoiceWindow, ButtonChoiceWindow, EntryWindow
from snackwich.exceptions import GotoPanelException, BreakSuccessionException

class Snackwich(object):
    config = None

    # A holder of arbitrary data that will be passed from callback to callback, 
    # if there are any.
    cb_context = { }

    # Some shorthand aliases to make the config nicer. These must be FROM'd 
    # into the current scope, above.
    aliases = { 'list':     ListboxChoiceWindow,
                'choice':   ButtonChoiceWindow,
                'entry':    EntryWindow
              }

    def __init__(self, config_filepath):
        self.__read_config(config_filepath)

    def __read_config(self, config_filepath):
        """Read and parse the given config file."""
    
        logging.info("Reading config from [%s]." % (config_filepath))
    
        try:
            with file(config_filepath) as f:
                raw_data = f.read()
        except:
            logging.exception("Could not read menu file-path [%s]." % 
                              (config_filepath))
            raise

        try:
            compiled = compile(raw_data, '<string>', 'exec')
            global_context = { '__builtins__': 
                                    __builtins__, 
                               'GotoPanelException': 
                                    GotoPanelException, 
                               'BreakSuccessionException': 
                                    BreakSuccessionException 
                             }

            eval(compiled, global_context, self.cb_context)
        except:
            logging.exception("Could not evaluate menu config from file-path "
                              "[%s]." % (config_filepath))
            raise

        if 'config' not in self.cb_context:
            message = "Config must assign itself to a variable named 'config'."
            
            logging.error(message)
            raise Exception(message)

        config = self.cb_context['config']

        if not isinstance(config, list):
            message = "Config from file-path [%s] is expected to be a list," \
                      "not [%s]." % (config_filepath, \
                                     config.__class__.__name__)

            logging.error(message)
            raise TypeError(message)

        self.config = config

    def __process_stanza(self, screen, key, expression, meta_attributes):
        """Process a single expression (form) from the config."""

        if 'widget' not in meta_attributes:
            message = "'_widget' value is not in the expression for key " \
                      "[%s]." % (key)

            logging.error(message)
            raise Exception(message)
    
        widget = meta_attributes['widget']

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

    def __get_current_key(self, expression):
        """For a given expression, validate the structure and return the key.
        """
    
        if isinstance(expression, tuple):
            if len(expression) != 2 or \
               not isinstance(expression[0], str) or \
               not callable(expression[1]):

                message = "As a tuple, an expression must be " \
                          "(<string>, <callable>)."

                logging.error(message)
                raise Exception(message)

            (key, expression_call) = expression
        elif not isinstance(expression, dict):
            message = "Expression is not a callable tuple, nor is it a " \
                      "dictionary."

            logging.error(message)
            raise Exception(message)
        else:
            if '_name' not in expression:
                message = "'_name' key not found in expression."

                logging.error(message)
                raise Exception(message)

            key = expression['_name']

        return key

    def __check_succession(self):
        """Run through the configured panel expressions and determine which 
        leads to which.
        """

        # Produce the succession of keys in a flat list, first (to avoid 
        # calculating each key more than once).

        i = 0
        keys = [ ]
        keys_r = { }
        for expression in self.config:
            try:
                key = self.__get_current_key(expression)
            except:
                logging.exception("Could not render key for expression (%d)." % 
                                  (i))
                raise

            keys.append(key)
            keys_r[key] = i
            i += 1

        num_expressions = len(self.config)
        succession = { }
        i = 0
        while i < num_expressions - 1:
            succession[keys[i]] = keys[i + 1]
            i += 1

        first_panel = keys[0] if succession else None

        return (succession, first_panel, keys, keys_r)

    def __slice_meta_attributes(self, dict_expression):
        meta_attributes = { }
        to_remove = [ ]
        for key in dict_expression:
            if key[0] == '_':
                meta_attributes[key[1:]] = dict_expression[key]
                to_remove.append(key)
        
        for key in to_remove:
            del dict_expression[key]

        return meta_attributes

    def execute(self):
        """Render each successive screen."""

        logging.info("Mapping panel succession.")

        try:
            (succession, first_key, _, keys_r) = self.__check_succession()
        except:
            logging.exception("Could not calculate panel succession.")
            raise

        results = { }

        # Make sure we actually had panels.
        if not first_key:
            return results;

        screen = SnackScreen()

        try:
            # Move through the panels in a linked-list fashion, so that we can 
            # reroute if told to.
        
            key = first_key
            while 1:
                logging.info("Processing panel expression with key [%s]." % 
                             (key))

                index = keys_r[key]
                expression = copy.deepcopy(self.config[index])

                # Allow there to be a function call or lambda that must be 
                # called to render the actual expression. This call will 
                # receive the past results as well as the current key. This 
                # will allow the current form to feed from previous forms.
                if isinstance(expression, tuple):
                    # The expression is a tuple with the key and a callback.
                
                    (key, expression_call) = expression

                    try:
                        expression = expression_call(key, results, \
                                                     self.cb_context)
                    except GotoPanelException as e:
                        # Go to a different panel.
                    
                        new_key = e.key
                        
                        logging.info("We were routed from panel with key [%s] "
                                     "to panel with key [%s]." % (key, 
                                                                  new_key))
                        
                        if key not in keys_r:
                            message = "We were told to go to panel with " \
                                      "invalid key [%s] while processing " \
                                      "panel with key [%s]." % (new_key, key)
                            
                            logging.error(message)
                            raise Exception(message)
                        
                        key = new_key
                        continue
                    except BreakSuccessionException as e:
                        # Break out of the menu.
                    
                        logging.info("We were told to stop presenting panels "
                                     "while process panel with key [%s]." % 
                                     (key))
                        break
                    except:
                        logging.exception("Callable expression for key [%s] " 
                                          "threw an exception." % (key))
                        raise

                    if not isinstance(expression, dict):
                        message = "Effective expression for key [%s] is not " \
                                  "a dictionary." % (key)
                        
                        logging.exception(message)
                        raise TypeError(message)
                else:
                    # The expression is a static dictionary.

                    key = expression['_name']
                    del expression['_name']

                try:
                    meta_attributes = self.__slice_meta_attributes(expression)
                except:
                    logging.exception("Could not slice meta-attributes from "
                                      "panel expression with key [%s]." % 
                                      (key))
                    raise

                logging.info("Processing expression with key [%s]." % (key))

                try:                
                    result = self.__process_stanza(screen, key, expression, 
                                                   meta_attributes)
                    
                    if key in results:
                        results[key].append(result)
                    else:
                        results[key] = [result]
                except:
                    logging.exception("There was an exception while processing"
                                      " the stanza for key [%s]." % (key))
                    raise

                # Were we directed to go to a different panel than what 
                # naturally comes next?
                if 'next' in meta_attributes:
                    next_key = meta_attributes['next']
                    
                    if key not in keys_r:
                        logging.error("Key [%s] set as next from panel with "
                                      "key [%s] does not refer to a valid "
                                      "panel." % (key))
                    
                    key = next_key
                else:
                    # Go to the next panel, or break if no more.
                    if key not in succession:
                        break

                    key = succession[key]
        except:
            logging.exception("There was an exception while processing "
                              "config stanza with key [%s]." % (key))
            raise
        finally:
            screen.finish()

        return results

