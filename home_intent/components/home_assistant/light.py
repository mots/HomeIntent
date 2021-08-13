from pathlib import Path

from home_intent import Intents

intents = Intents(__name__)


class Light:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("light.")]
        self.light_service = next(x for x in self.ha.services if x["domain"] == "light")

    @intents.dictionary_slots
    def light(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if x["state"] in ("on", "off")
        }
        return slots

    @intents.dictionary_slots
    def color(self):
        color_file = Path("home_intent/components/home_assistant/colors.txt")
        colors = color_file.read_text().strip().split("\n")
        return {color: color.replace(" ", "") for color in colors}

        # The original colors came from here:
        # self.light_service["services"]["turn_on"]["fields"]["color_name"]["selector"]["select"]["options"]

    @intents.sentences(["toggle the ($light) [light]", "turn (on|off) the ($light) [light]"])
    def toggle_light(self, light):
        self.ha.api.call_service("light", "toggle", {"entity_id": light})
        response = self.ha.api.get_entity(light)
        return f"Turning {response['state']} the {response['attributes']['friendly_name']} light"

    @intents.sentences(["(set | change | make) the ($light) [light] [to] ($color)"])
    def change_color(self, light, color):
        self.ha.api.call_service("light", "turn_on", {"entity_id": light, "color_name": color})
        response = self.ha.api.get_entity(light)
        return f"Setting the {response['attributes']['friendly_name']} to {color}"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] [to] ($color) [at] (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_color_brightness(self, light, color, brightness):
        self.ha.api.call_service(
            "light",
            "turn_on",
            {"entity_id": light, "color_name": color, "brightness_pct": brightness},
        )
        response = self.ha.api.get_entity(light)
        return f"Setting the {response['attributes']['friendly_name']} to {color} at {brightness}% brightness"

    @intents.sentences(
        [
            "(set | change | make) the ($light) [light] to (0..100){brightness} [percent] [brightness]"
        ]
    )
    def change_brightness(self, light, brightness):
        self.ha.api.call_service(
            "light", "turn_on", {"entity_id": light, "brightness_pct": brightness}
        )
        response = self.ha.api.get_entity(light)
        return f"Setting the {response['attributes']['friendly_name']} to {brightness}% brightness"

    # currently large number ranges throw a lot of things off. So no Kelvin for now! Maybe in the future!
    # @intents.sentences(
    #     [
    #         "(set | change | make | turn on) the ($light) [light] to (2000..6500,100){kelvin} [K] [kelvin]"
    #     ]
    # )
    # def change_kelvin(self, light, kelvin):
    #     self.ha.api.call_service("light", "turn_on", {"entity_id": light, "kelvin": kelvin})

    # @intents.sentences(
    #     [
    #         "(set | change | make | turn on) the ($light) [light] to (2000..6500,100){kelvin} [K] [kelvin] "
    #         "[at] (0..100){brightness} [percent] [brightness]"
    #     ]
    # )
    # def change_kelvin_brightness(self, light, kelvin, brightness):
    #     self.ha.api.call_service(
    #         "light", "turn_on", {"entity_id": light, "kelvin": kelvin, "brightness_pct": brightness}
    #     )
