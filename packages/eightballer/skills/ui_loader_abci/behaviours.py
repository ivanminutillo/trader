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
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.eightballer.skills.ui_loader_abci.models import Params
from packages.eightballer.skills.ui_loader_abci.rounds import (
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
            payload = ErrorPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class HealthcheckBehaviour(ComponentLoadingBaseBehaviour):
    """HealthcheckBehaviour"""

    matching_round: Type[AbstractRound] = HealthcheckRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = HealthcheckPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SetupBehaviour(ComponentLoadingBaseBehaviour):
    """SetupBehaviour"""

    matching_round: Type[AbstractRound] = SetupRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SetupPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ComponentLoadingRoundBehaviour(AbstractRoundBehaviour):
    """ComponentLoadingRoundBehaviour"""

    initial_behaviour_cls = SetupBehaviour
    abci_app_cls = ComponentLoadingAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        ErrorBehaviour,
        HealthcheckBehaviour,
        SetupBehaviour
    ]
