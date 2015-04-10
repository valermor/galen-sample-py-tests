
class DeviceConfig(object):

    def __init__(self, name, width, height, included_tags, excluded_tags, enabled):
        self.name = name
        self.width = width
        self.height = height
        self.included_tags = included_tags
        self.excluded_tags = excluded_tags
        self.enabled = enabled

    def __str__(self):
        return "name: " + self.name + "\n" +\
               "width: " + self.width + "\n" +\
               "height: " + self.height + "\n" +\
               "included tags: " + str(self.included_tags) + "\n" +\
               "excluded tags: " + str(self.excluded_tags) + "\n"

PHONE = DeviceConfig("mobile", "450", "800", ["mobile"], None, True)
TABLET = DeviceConfig("tablet", "750", "800", ["tablet"], None, True)
DESKTOP = DeviceConfig("desktop", "1024", "800", ["desktop"], None, True)

all_devices = [PHONE, TABLET, DESKTOP]

device_provider = tuple(filter(lambda x: x.enabled, all_devices))
