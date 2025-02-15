from enum import IntFlag, auto

from home_intent import Intents

intents = Intents(__name__)


class SupportedFeatures(IntFlag):
    SUPPORT_OPEN = auto()
    SUPPORT_CLOSE = auto()
    SUPPORT_SET_POSITION = auto()
    SUPPORT_STOP = auto()
    SUPPORT_OPEN_TILT = auto()
    SUPPORT_CLOSE_TILT = auto()
    SUPPORT_SET_TILT_POSITION = auto()
    SUPPORT_STOP_TILT = auto()


class Cover:
    def __init__(self, home_assistant):
        self.ha = home_assistant
        self.entities = [x for x in self.ha.entities if x["entity_id"].startswith("cover.")]
        self.cover_features = {
            x["entity_id"]: SupportedFeatures(x["attributes"].get("supported_features", 0))
            for x in self.entities
        }

    @intents.dictionary_slots
    def cover_open(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_OPEN in self.cover_features[x["entity_id"]]
            or SupportedFeatures.SUPPORT_OPEN_TILT in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_close(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_CLOSE in self.cover_features[x["entity_id"]]
            or SupportedFeatures.SUPPORT_CLOSE_TILT in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_set_position(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_SET_POSITION in self.cover_features[x["entity_id"]]
            or SupportedFeatures.SUPPORT_SET_TILT_POSITION in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_stop(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_STOP in self.cover_features[x["entity_id"]]
            or SupportedFeatures.SUPPORT_STOP_TILT in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_open_tilt(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_OPEN_TILT in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_close_tilt(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_CLOSE_TILT in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_set_tilt_position(self):
        slots = {
            f"{x['attributes'].get('friendly_name')}": x["entity_id"]
            for x in self.entities
            if SupportedFeatures.SUPPORT_SET_TILT_POSITION in self.cover_features[x["entity_id"]]
        }
        return slots

    @intents.dictionary_slots
    def cover_positions(self):
        slots = {"half way": 50}
        return slots

    @intents.sentences(["open [the] ($cover_open)"])
    def open_cover(self, cover_open):
        if SupportedFeatures.SUPPORT_OPEN in self.cover_features[cover_open]:
            self.ha.api.call_service("cover", "open_cover", {"entity_id": cover_open})
        elif SupportedFeatures.SUPPORT_OPEN_TILT in self.cover_features[cover_open]:
            self.ha.api.call_service("cover", "open_cover_tilt", {"entity_id": cover_open})
        response = self.ha.api.get_entity(cover_open)
        return f"Opening the {response['attributes']['friendly_name']}"

    @intents.sentences(["close [the] ($cover_close)"])
    def close_cover(self, cover_close):
        if SupportedFeatures.SUPPORT_CLOSE in self.cover_features[cover_close]:
            self.ha.api.call_service("cover", "close_cover", {"entity_id": cover_close})
        elif SupportedFeatures.SUPPORT_CLOSE_TILT in self.cover_features[cover_close]:
            self.ha.api.call_service("cover", "close_cover_tilt", {"entity_id": cover_close})
        response = self.ha.api.get_entity(cover_close)
        return f"Closing the {response['attributes']['friendly_name']}"

    @intents.sentences(["stop [the] ($cover_stop)"])
    def stop_cover(self, cover_stop):
        if SupportedFeatures.SUPPORT_STOP in self.cover_features[cover_stop]:
            self.ha.api.call_service("cover", "stop_cover", {"entity_id": cover_stop})
        if SupportedFeatures.SUPPORT_STOP_TILT in self.cover_features[cover_stop]:
            self.ha.api.call_service("cover", "stop_cover_tilt", {"entity_id": cover_stop})
        response = self.ha.api.get_entity(cover_stop)
        return f"Stopping the {response['attributes']['friendly_name']}"

    @intents.sentences(["tilt open [the] ($cover_open_tilt)"])
    def open_cover_tilt(self, cover_open_tilt):
        self.ha.api.call_service("cover", "open_cover_tilt", {"entity_id": cover_open_tilt})
        response = self.ha.api.get_entity(cover_open_tilt)
        return f"Opening the {response['attributes']['friendly_name']}"

    @intents.sentences(["tilt close [the] ($cover_close_tilt)"])
    def close_cover_tilt(self, cover_close_tilt):
        self.ha.api.call_service("cover", "close_cover_tilt", {"entity_id": cover_close_tilt})
        response = self.ha.api.get_entity(cover_close_tilt)
        return f"Closing the {response['attributes']['friendly_name']}"

    @intents.sentences(
        [
            "(set|change|make) [the] ($cover_set_position) [position] [to] ($cover_positions:!int) [percent]",
            "(open|close) [the] ($cover_set_position) [to] ($cover_positions:!int) [percent]",
        ]
    )
    def set_cover_position(self, cover_set_position, cover_positions):
        if SupportedFeatures.SUPPORT_SET_POSITION:
            self.ha.api.call_service(
                "cover",
                "set_cover_position",
                {"entity_id": cover_set_position, "position": cover_positions},
            )
        elif SupportedFeatures.SUPPORT_SET_TILT_POSITION:
            self.ha.api.call_service(
                "cover",
                "set_cover_tilt_position",
                {"entity_id": cover_set_position, "position": cover_positions},
            )
        response = self.ha.api.get_entity(cover_set_position)
        return f"Setting the {response['attributes']['friendly_name']} to {cover_positions}%"

    @intents.sentences(
        [
            "(set|change|make) [the] ($cover_set_tilt_position) tilt [position] [to] ($cover_positions:!int) [percent]",
            "tilt (open|close) [the] ($cover_set_tilt_position) [to] ($cover_positions:!int) [percent]",
        ]
    )
    def set_cover_tilt_position(self, cover_set_tilt_position, cover_positions):
        self.ha.api.call_service(
            "cover",
            "set_cover_tilt_position",
            {"entity_id": cover_set_tilt_position, "tilt_position": cover_positions},
        )
        response = self.ha.api.get_entity(cover_set_tilt_position)
        return f"Setting the {response['attributes']['friendly_name']} to {cover_positions}%"
