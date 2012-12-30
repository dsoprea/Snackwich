
import logging
import copy

from random import randint

from snack import SnackScreen

from snackwich.patch import ListboxChoiceWindow, ButtonChoiceWindow, \
                            EntryWindow
from snackwich.ui_functions import ProgressWindow, MessageWindow, \
                                   CheckboxListWindow
from snackwich.exceptions import GotoPanelException, \
                                 BreakSuccessionException, \
                                 QuitException, \
                                 RedrawException, \
                                 QuitAndExecuteException, \
                                 PostQuitAndExecuteException

class _PanelContainer(object):
    __config  = None
    __keys    = None
    __keys_r  = None
    __ns_keys = None

    def __init__(self, config):
        """
        config: List of panel expressions.
        """

        if config.__class__ != list:
            message = "Config must be a list."

            logging.error(message)
            raise TypeError(message)

        self.__config = []
        self.__keys = []
        self.__keys_r = {}
        self.__ns_keys = {}

        logging.info("Loading panels.")

        try:
            i = 0
            for expression in config:
                self.add(expression)
                i += 1
        except:
            logging.exception("Could not load panel (%d)." % (i))
            raise

    def exists(self, key):
    
        return (key in self.__keys_r)

    def get_index_by_key(self, key):

        return self.__keys_r[key]

    def get_copy_by_key(self, key):

        index = self.__keys_r[key]
        return copy.deepcopy(self.__config[index])

    def remove(self, key, ns=None):
        logging.info("Deregistering panel [%s] in namespace [%s]." % (key, ns))

        if key not in self.__keys_r:
            raise KeyError("Expression to be removed [%s] is not "
                           "registered." % (key))

        if ns != None:
            if ns not in self.__ns_keys:
                raise KeyError("Namespace [%s] is not valid for removal of "
                               "keys." % (ns))
        
            if key not in self.__ns_keys[ns]:
                raise KeyError("Panel [%s] is not indexed under namespace "
                               "[%s]. Can not remove." % (key, ns))

            self.__ns_keys[ns].remove(key)
            
            if not self.__ns_keys[ns]:
                del self.__ns_keys[ns]

        index = self.__keys_r[key]

        logging.debug("Removing panel [%s] with index [%d] under namespace "
                      "[%s]." % (key, index, ns))

        del self.__keys[index]
        del self.__keys_r[key]
        del self.__config[index]

        # Decrement the indices that we have for the panels currently having 
        # indices higher than the one that was deleted. 
        for other_key, other_index in self.__keys_r.items():
            if other_index > index:
                self.__keys_r[other_key] = other_index - 1

    def keys_in_ns(self, ns):
    
        return self.__ns_keys[ns][:] if ns in self.__ns_keys else []

    def remove_ns(self, ns):

        logging.info("Deregistering panels under namespace [%s]." % (ns))

        keys = self.keys_in_ns(ns)

        try:
            for key in keys:
                self.remove(key, ns)
        except:
            logging.exception("Could not remove all items under namespace "
                              "[%s]." % (ns))
            raise
        
        return keys

    def get_random_panel_name(self, kernel='Random'):

        while 1:
            key = ('%s_%d' % (kernel, randint(11111, 99999)))
            
            if key not in self.__keys_r:
                return key
        
    def add(self, expression, ns=None, assign_random_key=False):

        try:
            key = self.__get_current_key(expression)
        except:
            logging.exception("Could not render key for expression.")
            raise

        logging.info("Registering panel [%s]." % (key))

        if assign_random_key:
            if key != None:
                message = ("A random key can not be assigned because the key [%s] "
                           "was already defined." % (key))
                
                logging.exception(message)
                raise KeyError(message)

            key = self.get_random_panel_name()

        if not assign_random_key and key in self.__keys_r:
            raise KeyError("Expression [%s] already registered." % (key))

        new_index = len(self.__keys_r)

        self.__config.append(expression)
        self.__keys.append(key)
        self.__keys_r[key] = new_index

        if ns != None:
            if ns not in self.__ns_keys:
                self.__ns_keys[ns] = []

            self.__ns_keys[ns].append(key)

        return key

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

class Snackwich(object):
    __panels = None
    next_key = None
    results = None

    # Some shorthand aliases to make the config nicer. These must be FROM'd 
    # into the current scope, above.
    aliases = { 'list':      ListboxChoiceWindow,
                'choice':    ButtonChoiceWindow,
                'entry':     EntryWindow,
                'progress':  ProgressWindow,
                'message':   MessageWindow,
                'checklist': CheckboxListWindow,
              }

    def __init__(self, config):

        try:
            self.__panels = _PanelContainer(config)
        except:
            logging.exception("Could not build panel contaiment.")
            raise

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
            result = widget(screen=screen, **expression)
        except:
            logging.exception("Could not manufacture widget [%s] under key "
                              "[%s]." % (widget.__class__.__name__, key))
            raise

        screen.refresh()

        return result

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

    def __process_expression(self, expression, results, screen):

        # Allow there to be a function call or lambda that must be 
        # called to render the actual expression. This call will 
        # receive the past results as well as the current key. This 
        # will allow the current form to feed from previous forms.
        if isinstance(expression, tuple):
            # The expression is a tuple with the key and a callback.
        
            (key, expression_call) = expression

            try:
                expression = expression_call(self, key, results, 
                                             screen)
            except QuitException as e:
                logging.info("Post-callback for key [%s] has "
                             "requested emergency exit." % (key))
                
                return ('break', key, expression, True)
            except GotoPanelException as e:
                # Go to a different panel.
            
                new_key = e.key
                
                logging.info("We were routed from panel with key [%s] "
                             "to panel with key [%s]." % (key, 
                                                          new_key))
                
                if not self.__panels.exists(key):
                    message = "We were told to go to panel with " \
                              "invalid key [%s] while processing " \
                              "panel with key [%s]." % (new_key, key)
                    
                    logging.error(message)
                    raise Exception(message)
                
                key = new_key
                return ('continue', key, expression, False)
            except BreakSuccessionException as e:
                # Break out of the menu.
            
                logging.info("We were told to stop presenting panels "
                             "while processing panel with key [%s]." % 
                             (key))
                return ('break', key, expression, False)
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

        return (None, key, expression, False)

    def execute(self, first_key):
        """Display the panels. This resembles a state-machine, except that the 
        transitions can be determined on the fly.
        """

        self.results = { }

        screen = SnackScreen()

        try:
            # Move through the panels in a linked-list fashion, so that we can 
            # reroute if told to.
        
            key = first_key
            quit = False
            loop = True
            posthook_cb = None
            loophook_cb = None
            while loop:
                logging.info("Processing panel expression with key [%s]." % 
                             (key))

                try:
                    expression = self.__panels.get_copy_by_key(key)
                except:
                    logging.exception("Could not retrieve expression [%s]." % 
                                      (key))
                    raise

# Don't reprocess the expression more than once.
                result = self.__process_expression(expression, self.results, screen)
                (result_type, key, expression, quit_temp) = result
                
                if quit_temp:
                    quit = True

                if result_type == 'break':
                    break
                elif result_type == 'continue':
                    continue

                try:
                    meta_attributes = self.__slice_meta_attributes(expression)
                except:
                    logging.exception("Could not slice meta-attributes from "
                                      "panel expression with key [%s]." % 
                                      (key))
                    raise

                # Determine the panel to succeed this one. We do this early to 
                # allow callback to adjust this.
                self._next_key = meta_attributes['next'] \
                            if 'next' in meta_attributes \
                            else None
                
                if not self.__panels.exists(key):
                    logging.error("Key [%s] set as next from panel with "
                                  "key [%s] does not refer to a valid "
                                  "panel." % (key))
                
                logging.info("Processing expression with key [%s]." % (key))

                try:                
                    result = self.__process_stanza(screen, key, expression, 
                                                   meta_attributes)
# TODO: Move this to a separate call.
                    if 'post_cb' in meta_attributes:
                        callback = meta_attributes['post_cb']
                    
                        if not callable(callback):
                            message = ("Callback for key [%s] is not "
                                       "callable." % (key))
                            
                            logging.error(message)
                            raise Exception(message)

                        try:
                            result_temp = callback(self, key, result, 
                                                   expression, screen)
                            
                            # Allow them to adjust the result, but don't 
                            # require it to be returned.
                            if result_temp:
                                result = result_temp

                        except PostQuitAndExecuteException as e:

                            logging.info("Post-callback for key [%s] has "
                                         "requested an exit-and-execute." % 
                                         (key))
                            
                            # We can't break the loop the same way as 
                            # everything else, because we have a result that we 
                            # want to have registered. So, just allow us to 
                            # reach the end of the loop and prevent us from 
                            # looping again.
                            loop = False

                            posthook_cb = e.posthook_cb
                            result = e.result

                        except QuitAndExecuteException as e:
                        
                            logging.info("Post-callback for key [%s] has "
                                         "requested an exit-and-execute." % 
                                         (key))
                            
                            quit = True
                            posthook_cb = e.posthook_cb

                            break

                        except GotoPanelException as e:
                            # Go to a different panel.
                        
                            new_key = e.key
                            
                            logging.info("We were routed from panel with key "
                                         "[%s] to panel with key [%s] while in"
                                         " post callback." % (key, new_key))
                            
                            if not self.__panels.exists(key):
                                message = "We were told to go to panel with " \
                                          "invalid key [%s] while in post-" \
                                          "callback for panel with key " \
                                          "[%s]." % (new_key, key)
                                
                                logging.error(message)
                                raise Exception(message)
                            
                            key = new_key
                            continue

                        except RedrawException as e:
                            logging.info("Post-callback for key [%s] has "
                                         "requested a redraw." % (key))
                            
                            # Reset state values that might've been affected by 
                            # a callback.
                            
                            quit = False
                            self._next_key = None
                            
                            continue;

                        except QuitException as e:
                            logging.info("Post-callback for key [%s] has "
                                         "requested emergency exit." % (key))
                            
                            quit = True
                            break
                            
                        except BreakSuccessionException as e:
                            logging.info("Post-callback for key [%s] has "
                                         "instructed us to terminate." % (key))
                            break

                        except:
                            logging.exception("An exception occured in the "
                                              "post-callback for key [%s]." % 
                                              (key))
                            raise

                    # Static expression result handler.
                    else:
                        # If there's only one button, ignore what method they 
                        # used to close the window.
                        if 'buttons' in expression and \
                                len(expression['buttons']) > 1:
                            if 'is_esc' in result and result['is_esc'] or \
                               'button' in result and \
                                    result['button'] == 'cancel':
                                break

                    if 'collect_results' in meta_attributes and \
                            meta_attributes['collect_results']:
                        if key in self.results:
                            self.results[key].append(result)
                        else:
                            self.results[key] = [result]
                    else:
                        self.results[key] = result
                            
                except:
                    logging.exception("There was an exception while processing"
                                      " the stanza for key [%s]." % (key))
                    raise

                if self._next_key:
                    key = self._next_key
                else:
                    break
        except:
            logging.exception("There was an exception while processing "
                              "config stanza with key [%s]." % (key))
            raise
        finally:
            screen.finish()

        if posthook_cb:
            posthook_cb()

        return None if quit else self.results

    def get_next_panel(self):
        return self._next_key

    def set_next_panel(self, key):
        self._next_key = key

    def get_container(self):
        return self.__panels

    def get_results_for_ns(self, ns, allow_missing=False):
        results = {}
        for key in self.__panels.keys_in_ns(ns):
            try:
                results[key] = self.get_results(key)
            except KeyError:
                if not allow_missing:
                    raise

        return results

    def get_results(self, keys):
    
        if keys.__class__ == list:
            results = {}
            for key in keys:
                results[key] = self.results[key]

            return results
        else:
            return self.results[keys]

