# Intents class

The intents class is generally initiated at the top level of a component and has a bunch of decorators that make it easier to create intents and their components.

Example initialization:
```python
from home_intent import Intents
intents = Intents(__name__)
```

## `@intents.dictionary_slots`
Dictionary slots expect a dictionary of what is spoken to what is returned to the sentence method. It can be really useful to use entity id's to make for quick manipulation.

Example:
```python
@intents.dictionary_slots
def partial_time(self):
    return {
        "Bedroom Light": "light.bedroom",
        "Kitchen": "light.kitchen",
        "Office Light": "light.office",
    }
```


## `@intents.slots`
The regular slots are useful when the text that is spoken is the same as the text that is returned to the sentence method.

Example:
```python
@intents.slots
def shopping_item(self):
    return ["apples", "applesauce", "asparagus", "bacon"]
```

## `@intents.sentences(List[str])`
This decorator takes in a list of strings that can be spoken to trigger an intent. After the intent is triggered, the method that is decorated will execute. The sentences follow the [sentence structure](https://rhasspy.readthedocs.io/en/latest/training/) Rhasspy uses. 

Home Intent will parse out the slot name (in the form `($slotName)`) and tag name (in the form `{tagName}`) and verify they are parameters in the method. When an intent triggers, those values are then passed in to the method.

Example:
```python
@intents.sentences(["add ($shopping_item) to the [shopping] list"])
def add_item_to_shopping_list(self, shopping_item):
    self.ha.api.call_service("shopping_list", "add_item", {"name": shopping_item})
    return f"Adding {shopping_item} to the shopping list."
```

In the example `shopping_item` is expected to be passed in to the `add_item_to_shopping_list` based on the sentence. If a string is returned from the method, it will be spoken by Home Intent. For consistency and simplicity, all sentences that perform an action should start with a gerund. Examples:

 * Adding oreos to the shopping list
 * Setting the kitchen light to red
 * Turning on the bedroom light

and we're still figuring out how sentences that return state information should work, as very few of these are currently implemented.


## `@intents.on_event("register_sentences")`
This method registers a callback method that will be executed after the slot methods have been executed. It can come in handy for disabling an intent if there are no slots to execute on, which can help the overall experience as a sentence that can't do anything shouldn't be registered in Rhasspy. To aid in disabling intents, there are two helper methods `intents.disable_intent` and `intents.disable_all`.

!!!note "System Integrations"
    For system integrations (like Home Assistant), intents can also be disabled before calling `register` if it is known ahead of time if the group of intents is not going to be used.
    ```python
    if "shopping_list" in home_assistant_component.domains:
        home_intent.register(
            shopping_list.ShoppingList(home_assistant_component), shopping_list.intents
        )
    ```

### `intents.disable_intent(method)`
Disables a specific intent method. Takes in the actual method and will stop it from being registered in Rhasspy.

!!!note "On Disabling"
    By default any intent which have slots with no value will be disabled automatically in Rhasspy via Home Intent. This is to make writing components with specific features easier.

Example:
```python
@intents.on_event("register_sentences")
def conditionally_remove_intents(self):
    if reason_to_disable:
        intents.disable_intent(self.toggle_group)
```

### `intents.disable_all()`
Disables the entire intent. Can come in handy if there are no slots associated.

Example:
```python
@intents.on_event("register_sentences")
def conditionally_remove_intents(self):
    if reason_to_disable:
        intents.disable_all()
```

## On Slots and Sentences
One thing that is currently a little odd is that slot names (either regular or dictionary) have to be unique across Home Intent. Technically slots can be used across multiple intents. Sentences, on the other hand, do **not** need to be unique across Home Intent.

You will get a runtime error if multiple slots are found with the same name.
