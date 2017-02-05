class OpenAlprLocalEntity(ImageProcessingAlprEntity):
    """OpenAlpr local api entity."""

    def __init__(self, camera_entity, command, confidence, name=None):
        """Initialize openalpr local api."""
        super().__init__()

        self._cmd = command
        self._camera = camera_entity
        self._confidence = confidence

        if name:
            self._name = name
        else:
            self._name = "OpenAlpr {0}".format(
                split_entity_id(camera_entity)[1])

    @property
    def confidence(self):
        """Return minimum confidence for send events."""
        return self._confidence

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @asyncio.coroutine
    def async_process_image(self, image):
        """Process image.
        This method is a coroutine.
        """
        result = {}
        vehicles = 0

        alpr = yield from asyncio.create_subprocess_exec(
            *self._cmd,
            loop=self.hass.loop,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL
        )

        # send image
        stdout, _ = yield from alpr.communicate(input=image)
        stdout = io.StringIO(str(stdout, 'utf-8'))

        while True:
            line = stdout.readline()
            if not line:
                break

            new_plates = RE_ALPR_PLATE.search(line)
            new_result = RE_ALPR_RESULT.search(line)

            # found new vehicle
            if new_plates:
                vehicles += 1
                continue

            # found plate result
            if new_result:
                try:
                    result.update(
                        {new_result.group(1): float(new_result.group(2))})
                except ValueError:
                    continue

        self.async_process_plates(result, vehicles)
