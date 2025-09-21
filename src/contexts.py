class SolidFireIncompleteConfiguration(Exception):
    pass

class SolidFireSubordinateContext:
    def __init__(self, charm):
        self.charm = charm

    def __call__(self):
        config = self.charm.model.config
        ctxt = []
        missing = []

        required_keys = ['san_ip', 'san_login', 'san_password']

        for k in required_keys:
            if config.get(k):
                ctxt.append((k.replace('-', '_'), config[k]))
            else:
                missing.append(k)

        if missing:
            raise SolidFireIncompleteConfiguration(
                'Missing configuration: {}.'.format(missing)
            )

        section_name = self.charm.unit.name.replace('/', '-')
        vol_backend_name = self.charm.app.name
        ctxt.append(('volume_backend_name', vol_backend_name))
        ctxt.append(('volume_driver', 'cinder.volume.drivers.solidfire.SolidFireDriver'))

        return {
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {
                        section_name: ctxt,
                    },
                }
            }
        }