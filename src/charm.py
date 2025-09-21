import json
import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus
from ops.framework import StoredState

from contexts import SolidFireSubordinateContext

logger = logging.getLogger(__name__)


class CinderSolidFireCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.storage_backend_relation_joined, self._on_storage_backend_relation_joined)
        self.framework.observe(self.on.storage_backend_relation_changed, self._on_storage_backend_relation_changed)
        self._stored.set_default(backend_name=None)

    def _on_install(self, event):
        self.unit.status = ActiveStatus("Unit is ready")

    def _on_config_changed(self, event):
        # Re-emit relation data if config changes
        for relation in self.model.relations['storage-backend']:
            self._provide_backend_config(relation)

    def _on_storage_backend_relation_joined(self, event):
        self._provide_backend_config(event.relation)

    def _on_storage_backend_relation_changed(self, event):
        self._provide_backend_config(event.relation)

    def _provide_backend_config(self, relation):
        try:
            context = SolidFireSubordinateContext()
            config_data = context()
            backend_name = self.unit.name.replace('/', '-')
            relation.data[self.unit]['backend_name'] = backend_name
            relation.data[self.unit]['subordinate_configuration'] = json.dumps(config_data)
            relation.data[self.unit]['stateless'] = 'True'
            self._stored.backend_name = backend_name
        except Exception as e:
            logger.error(f"Failed to provide backend config: {e}")
            self.unit.status = ActiveStatus(f"Config error: {e}")


if __name__ == "__main__":
    main(CinderSolidFireCharm)