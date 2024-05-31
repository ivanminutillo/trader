# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains round behaviours of ComponentLoadingAbciApp."""

from abc import ABC
from glob import glob
from pathlib import Path
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.eightballer.skills.ui_loader_abci.models import Params
from packages.eightballer.skills.ui_loader_abci.rounds import (
    Event,
    SynchronizedData,
    ComponentLoadingAbciApp,
    ErrorRound,
    HealthcheckRound,
    SetupRound,
)
from packages.eightballer.skills.ui_loader_abci.rounds import (
    ErrorPayload,
    HealthcheckPayload,
    SetupPayload,
)


from aea.cli.utils.config import get_ipfs_node_multiaddr
from aea.skills.base import Model
from aea_cli_ipfs.ipfs_utils import DownloadError, IPFSTool


from enum import Enum

DEFAULT_FRONTEND_DIR = "frontend"

class HttpStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class ComponentLoadingBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the ui_loader_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class ErrorBehaviour(ComponentLoadingBaseBehaviour):
    """ErrorBehaviour"""

    matching_round: Type[AbstractRound] = ErrorRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            #  we check the parameters to see if we should alert the user via apprise.
            error_data = yield from self.get_error_data()
            if self.params.alert_user:
                yield from self.alert_user(error_data)
            payload = ErrorPayload(sender=sender, 
                                   error_data=error_data
                                   )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()
        self.set_done()

    def alert_user(self, error_data: str) -> bool:
        """Alert the user of the error."""
        # alert the user via apprise
        raise NotImplementedError
    
    def get_error_data(self) -> str:
        """Get the error data."""
        return f"Warning! Error detected: {self.synchronized_data.error_data} for {self.context.agent_address}"

    


class HealthcheckBehaviour(ComponentLoadingBaseBehaviour):
    """HealthcheckBehaviour"""

    matching_round: Type[AbstractRound] = HealthcheckRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            health_status = yield from self._check_ui_health()
            payload = HealthcheckPayload(sender=sender, 
                                      health_data=health_status
                                   )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()
        self.set_done()

    def _check_ui_health(self) -> bool:
        """Check the health of the UI."""
        status = HttpStatus.OK
        if status is HttpStatus.OK:
            yield Event.DONE
        yield Event.ERROR

class SetupBehaviour(ComponentLoadingBaseBehaviour):
    """SetupBehaviour"""

    matching_round: Type[AbstractRound] = SetupRound
    frontend_directory = Path(DEFAULT_FRONTEND_DIR)

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address

            ui_setup_ok = Event.DONE
            if self.params.user_interface_enabled:
                ui_name = self.params.user_interface_name
                self.context.logger.info(f"Loading User Interface: {ui_name}")
                ui_setup_ok = yield from self.load_ui()
            payload = SetupPayload(sender=sender, 
                                   setup_data=ui_setup_ok
                                   )
        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()
        self.set_done()

    # here we load the UI from the custom parameter passed in the setup payload

    def load_ui(self,) -> bool:
        """Load the UI from the setup_data."""
        # load the UI from 
        ipfs_tool = IPFSTool(get_ipfs_node_multiaddr())
        try:
            ipfs_tool.download(self.params.user_interface_ipfs_hash, DEFAULT_FRONTEND_DIR)
        except DownloadError as e:
            self.context.logger.error(str(e))
            self.context.logger.error("Failed to download frontend from IPFS.")
            yield Event.ERROR

        # we generate a mapping of routes based on all the files found in the frontend directory
        self.context.logger.info("Generating routes...")
        self.context.shared_state["routes"] = self.generate_routes()
        self.context.logger.info("Routes generated.")
        yield Event.DONE

    def generate_routes(self) -> dict:
        """
        We generate a mapping of routes based on all the files found in the frontend directory.
        We read the files into memory and store them in the routes dict.
        """
        routes = {}
        for path in glob(f"{self.frontend_directory}/**/*", recursive=True):
            data = Path(path)
            if data.is_file():
                route = data.relative_to(self.frontend_directory / "build")
                routes[str(route)] = data.read_bytes()
        return routes



class ComponentLoadingRoundBehaviour(AbstractRoundBehaviour):
    """ComponentLoadingRoundBehaviour"""

    initial_behaviour_cls = SetupBehaviour
    abci_app_cls = ComponentLoadingAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        ErrorBehaviour,
        HealthcheckBehaviour,
        SetupBehaviour
    ]
